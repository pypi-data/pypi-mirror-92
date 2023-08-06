import logging
from abc import ABCMeta, abstractmethod

import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler

from abcpy.acceptedparametersmanager import *
from abcpy.graphtools import GraphTools
# import dataset and networks definition:
from abcpy.statistics import LinearTransformation

# Different torch components
try:
    import torch
except ImportError:
    has_torch = False
else:
    has_torch = True
    from abcpy.NN_utilities.networks import createDefaultNN, ScalerAndNet
    from abcpy.statistics import NeuralEmbedding

from abcpy.NN_utilities.algorithms import FP_nn_training, triplet_training, contrastive_training
from abcpy.NN_utilities.utilities import compute_similarity_matrix


# TODO: there seems to be issue when n_samples_per_param >1. Check that. Should you modify the _sample_parameters-statistics function?

class StatisticsLearning(metaclass=ABCMeta):
    """This abstract base class defines a way to choose the summary statistics.
    """

    def __init__(self, model, statistics_calc, backend, n_samples=1000, n_samples_val=0, n_samples_per_param=1,
                 parameters=None, simulations=None, parameters_val=None, simulations_val=None, seed=None):

        """The constructor of a sub-class must accept a non-optional model, statistics calculator and
        backend which are stored to self.model, self.statistics_calc and self.backend. Further it
        accepts two optional parameters n_samples and seed defining the number of simulated dataset
        used for the pilot to decide the summary statistics and the integer to initialize the random
        number generator.

        This __init__ takes care of sample-statistics generation, with the parallelization; however, you can choose
        to provide simulations and corresponding parameters that have been previously generated, with the parameters
        `parameters` and `simulations`.

        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_cal: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set. Default
            value is None.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        """
        if (parameters is None) != (simulations is None):
            raise RuntimeError("parameters and simulations need to be provided together.")

        if (parameters_val is None) != (simulations_val is None):
            raise RuntimeError("parameters_val and simulations_val need to be provided together.")

        self.model = model
        self.statistics_calc = statistics_calc
        self.backend = backend
        self.rng = np.random.RandomState(seed)
        self.n_samples_per_param = n_samples_per_param
        self.logger = logging.getLogger(__name__)

        n_samples_to_generate = n_samples * (parameters is None) + n_samples_val * (parameters_val is None)

        if n_samples_to_generate > 0:  # need to generate some data
            self.logger.info('Generation of data...')

            self.logger.debug("Definitions for parallelization.")
            # An object managing the bds objects
            self.accepted_parameters_manager = AcceptedParametersManager(self.model)
            self.accepted_parameters_manager.broadcast(self.backend, [])

            self.logger.debug("Map phase.")
            # main algorithm
            seed_arr = self.rng.randint(1, n_samples_to_generate * n_samples_to_generate, size=n_samples_to_generate,
                                        dtype=np.int32)
            rng_arr = np.array([np.random.RandomState(seed) for seed in seed_arr])
            rng_pds = self.backend.parallelize(rng_arr)

            self.logger.debug("Collect phase.")
            sample_parameters_statistics_pds = self.backend.map(self._sample_parameter_statistics, rng_pds)

            sample_parameters_and_statistics = self.backend.collect(sample_parameters_statistics_pds)
            sample_parameters, sample_statistics = [list(t) for t in zip(*sample_parameters_and_statistics)]
            sample_parameters = np.array(sample_parameters)
            self.sample_statistics = np.concatenate(sample_statistics)

            self.logger.debug("Reshape data")
            # reshape the sample parameters; so that we can also work with multidimensional parameters
            self.sample_parameters = sample_parameters.reshape((n_samples_to_generate, -1))

            # now reshape the statistics in the case in which several n_samples_per_param > 1, and repeat the array with
            # the parameters so that the regression algorithms can work on the pair of arrays. Maybe there are smarter
            # ways of doing this.

            sample_statistics_generated = self.sample_statistics.reshape(
                n_samples_to_generate * self.n_samples_per_param, -1)
            sample_parameters_generated = np.repeat(self.sample_parameters, self.n_samples_per_param, axis=0)
            # now split between train and validation set:
            self.sample_statistics = sample_statistics_generated[
                                     0: n_samples * self.n_samples_per_param * (parameters is None)]
            self.sample_parameters = sample_parameters_generated[
                                     0: n_samples * self.n_samples_per_param * (parameters is None)]

            self.sample_statistics_val = sample_statistics_generated[
                                         n_samples * self.n_samples_per_param * (parameters is None):len(
                                             sample_statistics_generated)]
            self.sample_parameters_val = sample_parameters_generated[
                                         n_samples * self.n_samples_per_param * (parameters is None):len(
                                             sample_parameters_generated)]

            self.logger.info('Data generation finished.')

        if parameters is not None:
            # do all the checks on dimensions:
            if not isinstance(parameters, np.ndarray) or not isinstance(simulations, np.ndarray):
                raise TypeError("parameters and simulations need to be numpy arrays.")
            if len(parameters.shape) != 2:
                raise RuntimeError("parameters have to be a 2-dimensional array")
            if len(simulations.shape) != 2:
                raise RuntimeError("simulations have to be a 2-dimensional array")
            if simulations.shape[0] != parameters.shape[0]:
                raise RuntimeError("parameters and simulations need to have the same first dimension")

            # if all checks are passed:
            self.sample_statistics = self.statistics_calc.statistics(
                [simulations[i] for i in range(simulations.shape[0])])
            self.sample_parameters = parameters

            self.logger.info("The statistics will be learned using the provided data and parameters")

        if parameters_val is not None:
            # do all the checks on dimensions:
            if not isinstance(parameters_val, np.ndarray) or not isinstance(simulations_val, np.ndarray):
                raise TypeError("parameters_val and simulations_val need to be numpy arrays.")
            if len(parameters_val.shape) != 2:
                raise RuntimeError("parameters_val have to be a 2-dimensional array")
            if len(simulations_val.shape) != 2:
                raise RuntimeError("simulations_val have to be a 2-dimensional array")
            if simulations_val.shape[0] != parameters_val.shape[0]:
                raise RuntimeError("parameters_val and simulations_val need to have the same first dimension")

            # if all checks are passed:
            self.sample_statistics_val = self.statistics_calc.statistics(
                [simulations_val[i] for i in range(simulations_val.shape[0])])
            self.sample_parameters_val = parameters_val

            self.logger.info("The provided validation data and parameters will be used as a validation set.")

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['backend']
        return state

    @abstractmethod
    def get_statistics(self):
        """
        This should return a statistics object that implements the learned transformation.

        Returns
        -------
        abcpy.statistics.Statistics object
            a statistics object that implements the learned transformation.
        """
        raise NotImplementedError

    def _sample_parameter_statistics(self, rng=np.random.RandomState()):
        """Function that generates (parameter, statistics). It is mapped to the different workers during data
        generation.
        """
        self.sample_from_prior(rng=rng)
        parameter = self.get_parameters()
        y_sim = self.simulate(self.n_samples_per_param, rng=rng)
        if y_sim is not None:
            statistics = self.statistics_calc.statistics(y_sim)
        return parameter, statistics


class Semiautomatic(StatisticsLearning, GraphTools):
    """This class implements the semi automatic summary statistics learning technique described in Fearnhead and
    Prangle [1].

    [1] Fearnhead P., Prangle D. 2012. Constructing summary statistics for approximate
    Bayesian computation: semi-automatic approximate Bayesian computation. J. Roy. Stat. Soc. B 74:419–474.
    """

    def __init__(self, model, statistics_calc, backend, n_samples=1000, n_samples_per_param=1, parameters=None,
                 simulations=None, seed=None):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_cal: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed. Default value is None.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        """
        # the sampling is performed by the init of the parent class
        super(Semiautomatic, self).__init__(model, statistics_calc, backend,
                                            n_samples, n_samples_per_param=n_samples_per_param, parameters=parameters,
                                            simulations=simulations, seed=seed)

        self.logger.info('Learning of the transformation...')

        self.coefficients_learnt = np.zeros(shape=(self.sample_parameters.shape[1], self.sample_statistics.shape[1]))
        regr = linear_model.LinearRegression(fit_intercept=True)
        for ind in range(self.sample_parameters.shape[1]):
            regr.fit(self.sample_statistics, self.sample_parameters[:, ind])
            self.coefficients_learnt[ind, :] = regr.coef_

        self.logger.info("Finished learning the transformation.")

    def get_statistics(self):
        """
        Returns an abcpy.statistics.LinearTransformation Statistics implementing the learned transformation.

        Returns
        -------
        abcpy.statistics.LinearTransformation object
            a statistics object that implements the learned transformation.
        """
        return LinearTransformation(np.transpose(self.coefficients_learnt), previous_statistics=self.statistics_calc)


class StatisticsLearningNN(StatisticsLearning, GraphTools):
    """This is the base class for all the statistics learning techniques involving neural networks. In most cases, you
    should not instantiate this directly. The actual classes instantiate this with the right arguments.

    In order to use this technique, Pytorch is required to handle the neural networks.
    """

    def __init__(self, model, statistics_calc, backend, training_routine, distance_learning, embedding_net=None,
                 n_samples=1000, n_samples_val=0, n_samples_per_param=1, parameters=None, simulations=None,
                 parameters_val=None, simulations_val=None, seed=None, cuda=None, scale_samples=True, quantile=0.1,
                 **training_routine_kwargs):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_cal: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        training_routine: function
            training routine to train the network. It has to take as first and second arguments the matrix of
            simulations and the corresponding targets (or the similarity matrix if `distance_learning` is True). It also
            needs to have as keyword parameters embedding_net and cuda.
        distance_learning: boolean
            this has to be True if the statistics learning technique is based on distance learning, in which case the
            __init__ computes the similarity matrix.
        embedding_net: torch.nn object or list
            it can be a torch.nn object with input size corresponding to size of model output, alternatively, a list
            with integer numbers denoting the width of the hidden layers, from which a fully connected network with
            that structure is created, having the input and output size corresponding to size of model output and
            number of parameters. In case this is None, the depth of the network and the width of the hidden layers is
            determined from the input and output size as specified in abcpy.NN_utilities.networks.DefaultNN.
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set. Default
            value is None.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        scale_samples: boolean, optional
            If True, a scaler of the class `sklearn.preprocessing.MinMaxScaler` will be fit on the training data before 
            neural network training, and training and validation data simulations data will be rescaled. 
            When calling the `get_statistics` method, 
            a network of the class `ScalerAndNet` will be used in instantiating the statistics; this network is a 
            wrapper of a neural network and a scaler and transforms the data with the scaler before applying the neural
            network.  
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        quantile: float, optional
            quantile used to define the similarity set if distance_learning is True. Default to 0.1.
        training_routine_kwargs:
            additional kwargs to be passed to the underlying training routine.
        """
        self.logger = logging.getLogger(__name__)
        self.scale_samples = scale_samples

        # Define device
        if not has_torch:
            raise ImportError(
                "Pytorch is required to instantiate an element of the {} class, in order to handle "
                "neural networks. Please install it. ".format(self.__class__.__name__))

        # set random seed for torch as well:
        if seed is not None:
            torch.manual_seed(seed)

        if cuda is None:
            cuda = torch.cuda.is_available()
        elif cuda and not torch.cuda.is_available():
            # if the user requested to use GPU but no GPU is there
            cuda = False
            self.logger.warning(
                "You requested to use GPU but no GPU is available! The computation will proceed on CPU.")

        self.device = "cuda" if cuda and torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            self.logger.debug("We are using GPU to train the network.")
        else:
            self.logger.debug("We are using CPU to train the network.")

        # this handles generation of the data (or its formatting in case the data is provided to the Semiautomatic
        # class)
        super(StatisticsLearningNN, self).__init__(model, statistics_calc, backend, n_samples, n_samples_val,
                                                   n_samples_per_param, parameters, simulations, seed=seed,
                                                   parameters_val=parameters_val, simulations_val=simulations_val)

        # we have a validation set if it has the following attribute with size larger than 0
        has_val_set = hasattr(self, "sample_parameters_val") and len(self.sample_parameters_val) > 0

        self.logger.info('Learning of the transformation...')
        # Define Data
        target, simulations = self.sample_parameters, self.sample_statistics
        if has_val_set:
            target_val, simulations_val = self.sample_parameters_val, self.sample_statistics_val
        else:
            target_val, simulations_val = None, None

        if distance_learning:
            self.logger.debug("Computing similarity matrix...")
            # define the similarity set
            similarity_set = compute_similarity_matrix(target, quantile)
            if has_val_set:
                similarity_set_val = compute_similarity_matrix(target_val, quantile)
            else:
                similarity_set_val = None
            self.logger.debug("Done")

        # set up the scaler and transform the data:
        if self.scale_samples:
            self.scaler = MinMaxScaler().fit(simulations)
            simulations = self.scaler.transform(simulations)
            if has_val_set:
                simulations_val = self.scaler.transform(simulations_val)

        # now setup the default neural network or not

        if isinstance(embedding_net, torch.nn.Module):
            self.embedding_net = embedding_net
            self.logger.debug('We use the provided neural network')

        elif isinstance(embedding_net, list) or embedding_net is None:
            # therefore we need to generate the neural network given the list. The following function returns a class
            # of NN with given input size, output size and hidden sizes; then, need () to instantiate the network
            self.embedding_net = createDefaultNN(input_size=simulations.shape[1], output_size=target.shape[1],
                                                 hidden_sizes=embedding_net)()
            self.logger.debug('We generate a default neural network')

        if cuda:
            self.embedding_net.cuda()

        self.logger.debug('We now run the training routine')

        if distance_learning:
            self.embedding_net = training_routine(simulations, similarity_set, embedding_net=self.embedding_net,
                                                  cuda=cuda, samples_val=simulations_val,
                                                  similarity_set_val=similarity_set_val, **training_routine_kwargs)
        else:
            self.embedding_net = training_routine(simulations, target, embedding_net=self.embedding_net,
                                                  cuda=cuda, samples_val=simulations_val, target_val=target_val,
                                                  **training_routine_kwargs)

        self.logger.info("Finished learning the transformation.")

        self.embedding_net.cpu()  # move back the net to CPU.

    def get_statistics(self):
        """
        Returns a NeuralEmbedding Statistics implementing the learned transformation.

        If a scaler was used, the `net` attribute of the returned object is of the class `ScalerAndNet`, which is a
        nn.Module object wrapping the scaler and the learned neural network and applies the scaler before the data is
        fed through the neural network.

        Returns
        -------
        abcpy.statistics.NeuralEmbedding object
            a statistics object that implements the learned transformation.
        """
        if self.scale_samples:
            return NeuralEmbedding(net=ScalerAndNet(self.embedding_net, self.scaler),
                                   previous_statistics=self.statistics_calc)
        else:
            return NeuralEmbedding(net=self.embedding_net, previous_statistics=self.statistics_calc)


# the following classes subclass the base class StatisticsLearningNN with different training routines

class SemiautomaticNN(StatisticsLearningNN):
    """This class implements the semi automatic summary statistics learning technique as described in
     Jiang et al. 2017 [1].

     In order to use this technique, Pytorch is required to handle the neural networks.

     [1] Jiang, B., Wu, T.Y., Zheng, C. and Wong, W.H., 2017. Learning summary statistic for approximate Bayesian
     computation via deep neural network. Statistica Sinica, pp.1595-1618.
    """

    def __init__(self, model, statistics_calc, backend, embedding_net=None, n_samples=1000, n_samples_val=0,
                 n_samples_per_param=1, parameters=None, simulations=None, parameters_val=None, simulations_val=None,
                 early_stopping=False, epochs_early_stopping_interval=1, start_epoch_early_stopping=10,
                 seed=None, cuda=None, scale_samples=True, batch_size=16, n_epochs=200, load_all_data_GPU=False,
                 lr=1e-3, optimizer=None,
                 scheduler=None, start_epoch_training=0, optimizer_kwargs={}, scheduler_kwargs={}, loader_kwargs={}):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_cal: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        embedding_net: torch.nn object or list
            it can be a torch.nn object with input size corresponding to size of model output and output size
            corresponding to the number of parameters or, alternatively, a list with integer numbers denoting the width
            of the hidden layers, from which a fully connected network with that structure is created, having the input
            and output size corresponding to size of model output and number of parameters. In case this is None, the
            depth of the network and the width of the hidden layers is determined from the input and output size as
            specified in abcpy.NN_utilities.networks.DefaultNN.
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set. Default
            value is None.
        early_stopping: boolean, optional
            If True, the validation set (which needs to be either provided through the arguments `parameters_val` and
            `simulations_val` or generated by setting `n_samples_val` to a value larger than 0) is used to early stop
            the training of the neural network as soon as the loss on the validation set starts to increase. Default
            value is False.
        epochs_early_stopping_interval: integer, optional
            The frequency at which the validation error is compared in order to decide whether to early stop the
            training or not. Namely, if `epochs_early_stopping_interval=10`, early stopping can happen only at epochs multiple of
            10. Defaul value is 1.
        start_epoch_early_stopping: integer, optional
            The epoch after which early stopping can happen; in fact, as soon as training starts, there may be a 
            transient period in which the loss increases. Default value is 10.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        scale_samples: boolean, optional
            If True, a scaler of the class `sklearn.preprocessing.MinMaxScaler` will be fit on the training data before 
            neural network training, and training and validation data simulations data will be rescaled. 
            When calling the `get_statistics` method, 
            a network of the class `ScalerAndNet` will be used in instantiating the statistics; this network is a 
            wrapper of a neural network and a scaler and transforms the data with the scaler before applying the neural
            network.  
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        batch_size: integer, optional
            the batch size used for training the neural network. Default is 16
        n_epochs: integer, optional
            the number of epochs used for training the neural network. Default is 200
        load_all_data_GPU: boolean, optional
            If True and if we a GPU is used, the whole dataset is loaded on the GPU before training begins; this may
            speed up training as it avoid transfer between CPU and GPU, but it is not guaranteed to do. Note that if the
            dataset is not small enough, setting this to True causes things to crash if the dataset is too large.
            Default to False, you should not rely too much on this.
        lr: float, optional
            The learning rate to be used in the iterative training scheme of the neural network. Default to 1e-3.
        optimizer: torch Optimizer class, optional
            A torch Optimizer class, for instance `SGD` or `Adam`. Default to `Adam`. Additional parameters may be
            passed through the `optimizer_kwargs` parameter.
        scheduler: torch _LRScheduler class, optional
            A torch _LRScheduler class, used to modify the learning rate across epochs. By default, no scheduler is
            used. Additional parameters may be passed through the `scheduler_kwargs` parameter.
        start_epoch_training: integer, optional
            If a scheduler is provided, for the first `start_epoch_training` epochs the scheduler is applied to modify
            the learning rate without training the network. From then on, the training proceeds normally, applying both
            the scheduler and the optimizer at each epoch. Default to 0.
        verbose: boolean, optional
            if True, prints more information from the training routine. Default to False.
        optimizer_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the optimizer.
        scheduler_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the scheduler.
        loader_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the loader (that handles loading the samples from the
            dataset during the training phase).
        """
        super(SemiautomaticNN, self).__init__(model, statistics_calc, backend, FP_nn_training, distance_learning=False,
                                              embedding_net=embedding_net, n_samples=n_samples,
                                              n_samples_val=n_samples_val, n_samples_per_param=n_samples_per_param,
                                              parameters=parameters, simulations=simulations,
                                              parameters_val=parameters_val, simulations_val=simulations_val,
                                              early_stopping=early_stopping,
                                              epochs_early_stopping_interval=epochs_early_stopping_interval,
                                              start_epoch_early_stopping=start_epoch_early_stopping,
                                              seed=seed, cuda=cuda, scale_samples=scale_samples, batch_size=batch_size,
                                              n_epochs=n_epochs, load_all_data_GPU=load_all_data_GPU, lr=lr,
                                              optimizer=optimizer, scheduler=scheduler,
                                              start_epoch_training=start_epoch_training,
                                              optimizer_kwargs=optimizer_kwargs,
                                              scheduler_kwargs=scheduler_kwargs, loader_kwargs=loader_kwargs)


class TripletDistanceLearning(StatisticsLearningNN):
    """This class implements the statistics learning technique by using the triplet loss [1] for distance learning as
     described in Pacchiardi et al. 2019 [2].

     In order to use this technique, Pytorch is required to handle the neural networks.

     [1] Schroff, F., Kalenichenko, D. and Philbin, J., 2015. Facenet: A unified embedding for face recognition and
     clustering. In Proceedings of the IEEE conference on computer vision and pattern recognition (pp. 815-823).

     [2] Pacchiardi, L., Kunzli, P., Schoengens, M., Chopard, B. and Dutta, R., 2019. Distance-learning For Approximate
     Bayesian Computation To Model a Volcanic Eruption. arXiv preprint arXiv:1909.13118.
    """

    def __init__(self, model, statistics_calc, backend, embedding_net=None, n_samples=1000, n_samples_val=0,
                 n_samples_per_param=1, parameters=None, simulations=None, parameters_val=None, simulations_val=None,
                 early_stopping=False, epochs_early_stopping_interval=1, start_epoch_early_stopping=10, seed=None,
                 cuda=None, scale_samples=True,
                 quantile=0.1, batch_size=16, n_epochs=200, load_all_data_GPU=False, margin=1., lr=None, optimizer=None,
                 scheduler=None, start_epoch_training=0, optimizer_kwargs={}, scheduler_kwargs={}, loader_kwargs={}):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_cal: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        embedding_net: torch.nn object or list
            it can be a torch.nn object with input size corresponding to size of model output (output size can be any);
            alternatively, a list with integer numbers denoting the width of the hidden layers, from which a fully
            connected network with that structure is created, having the input and output size corresponding to size of
            model output and number of parameters. In case this is None, the depth of the network and the width of the
            hidden layers is determined from the input and output size as specified in
            abcpy.NN_utilities.networks.DefaultNN.
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_val: int, optional
            The number of (parameter, simulated data) tuple to be generated to be used as a validation set in the pilot
            step. The default value is 0, which means no validation set is used.
            This is ignored if `simulations_val` and `parameters_val` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed to generate the training data. Default value is None.
        parameters_val: array, optional
            A numpy array with shape (n_samples_val, n_parameters) that is used, together with `simulations_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `simulations_val`, in which case no other simulations are performed to generate the validation set. Default 
            value is None.
        simulations_val: array, optional
            A numpy array with shape (n_samples_val, output_size) that is used, together with `parameters_val` as a 
            validation set in the summary selection learning algorithm. It has to be provided together with 
            `parameters_val`, in which case no other simulations are performed to generate the validation set. Default
            value is None.
        early_stopping: boolean, optional
            If True, the validation set (which needs to be either provided through the arguments `parameters_val` and
            `simulations_val` or generated by setting `n_samples_val` to a value larger than 0) is used to early stop
            the training of the neural network as soon as the loss on the validation set starts to increase. Default
            value is False.
        epochs_early_stopping_interval: integer, optional
            The frequency at which the validation error is compared in order to decide whether to early stop the
            training or not. Namely, if `epochs_early_stopping_interval=10`, early stopping can happen only at epochs
            multiple of 10. Defaul value is 1.
        start_epoch_early_stopping: integer, optional
            The epoch after which early stopping can happen; in fact, as soon as training starts, there may be a 
            transient period in which the loss increases. Default value is 10.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        scale_samples: boolean, optional
            If True, a scaler of the class `sklearn.preprocessing.MinMaxScaler` will be fit on the training data before 
            neural network training, and training and validation data simulations data will be rescaled. 
            When calling the `get_statistics` method, 
            a network of the class `ScalerAndNet` will be used in instantiating the statistics; this network is a 
            wrapper of a neural network and a scaler and transforms the data with the scaler before applying the neural
            network.  
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        quantile: float, optional
            quantile used to define the similarity set if distance_learning is True. Default to 0.1.
        batch_size: integer, optional
            the batch size used for training the neural network. Default is 16
        n_epochs: integer, optional
            the number of epochs used for training the neural network. Default is 200
        load_all_data_GPU: boolean, optional
            If True and if we a GPU is used, the whole dataset is loaded on the GPU before training begins; this may
            speed up training as it avoid transfer between CPU and GPU, but it is not guaranteed to do. Note that if the
            dataset is not small enough, setting this to True causes things to crash if the dataset is too large.
            Default to False, you should not rely too much on this.
        margin: float, optional
            margin defining the triplet loss. The larger it is, the further away dissimilar samples are pushed with
            respect to similar ones. Default to 1.
        lr: float, optional
            The learning rate to be used in the iterative training scheme of the neural network. Default to 1e-3.
        optimizer: torch Optimizer class, optional
            A torch Optimizer class, for instance `SGD` or `Adam`. Default to `Adam`. Additional parameters may be
            passed through the `optimizer_kwargs` parameter.
        scheduler: torch _LRScheduler class, optional
            A torch _LRScheduler class, used to modify the learning rate across epochs. By default, no scheduler is
            used. Additional parameters may be passed through the `scheduler_kwargs` parameter.
        start_epoch_training: integer, optional
            If a scheduler is provided, for the first `start_epoch_training` epochs the scheduler is applied to modify
            the learning rate without training the network. From then on, the training proceeds normally, applying both
            the scheduler and the optimizer at each epoch. Default to 0.
        verbose: boolean, optional
            if True, prints more information from the training routine. Default to False.
        optimizer_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the optimizer.
        scheduler_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the scheduler.
        loader_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the loader (that handles loading the samples from the
            dataset during the training phase).
        """

        super(TripletDistanceLearning, self).__init__(model, statistics_calc, backend, triplet_training,
                                                      distance_learning=True, embedding_net=embedding_net,
                                                      n_samples=n_samples, n_samples_val=n_samples_val,
                                                      n_samples_per_param=n_samples_per_param,
                                                      parameters=parameters, simulations=simulations,
                                                      parameters_val=parameters_val, simulations_val=simulations_val,
                                                      early_stopping=early_stopping,
                                                      epochs_early_stopping_interval=epochs_early_stopping_interval,
                                                      start_epoch_early_stopping=start_epoch_early_stopping,
                                                      seed=seed, cuda=cuda, scale_samples=scale_samples,
                                                      quantile=quantile, batch_size=batch_size,
                                                      n_epochs=n_epochs, load_all_data_GPU=load_all_data_GPU,
                                                      margin=margin, lr=lr, optimizer=optimizer, scheduler=scheduler,
                                                      start_epoch_training=start_epoch_training,
                                                      optimizer_kwargs=optimizer_kwargs,
                                                      scheduler_kwargs=scheduler_kwargs, loader_kwargs=loader_kwargs)


class ContrastiveDistanceLearning(StatisticsLearningNN):
    """This class implements the statistics learning technique by using the contrastive loss [1] for distance learning
     as described in Pacchiardi et al. 2019 [2].

     In order to use this technique, Pytorch is required to handle the neural networks.

     [1] Hadsell, R., Chopra, S. and LeCun, Y., 2006, June. Dimensionality reduction by learning an invariant mapping.
     In 2006 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR'06) (Vol. 2,
     pp. 1735-1742). IEEE.

     [2] Pacchiardi, L., Kunzli, P., Schoengens, M., Chopard, B. and Dutta, R., 2019. Distance-learning For Approximate
     Bayesian Computation To Model a Volcanic Eruption. arXiv preprint arXiv:1909.13118.
    """

    def __init__(self, model, statistics_calc, backend, embedding_net=None, n_samples=1000, n_samples_val=0,
                 n_samples_per_param=1, parameters=None, simulations=None, parameters_val=None, simulations_val=None,
                 early_stopping=False, epochs_early_stopping_interval=1, start_epoch_early_stopping=10, seed=None,
                 cuda=None, scale_samples=True, quantile=0.1, batch_size=16, n_epochs=200, positive_weight=None,
                 load_all_data_GPU=False, margin=1., lr=None, optimizer=None, scheduler=None,
                 start_epoch_training=0, optimizer_kwargs={}, scheduler_kwargs={}, loader_kwargs={}):
        """
        Parameters
        ----------
        model: abcpy.models.Model
            Model object that conforms to the Model class.
        statistics_cal: abcpy.statistics.Statistics
            Statistics object that conforms to the Statistics class.
        backend: abcpy.backends.Backend
            Backend object that conforms to the Backend class.
        embedding_net: torch.nn object or list
            it can be a torch.nn object with input size corresponding to size of model output (output size can be any);
            alternatively, a list with integer numbers denoting the width of the hidden layers, from which a fully
            connected network with that structure is created, having the input and output size corresponding to size of
            model output and number of parameters. In case this is None, the depth of the network and the width of the
            hidden layers is determined from the input and output size as specified in
            abcpy.NN_utilities.networks.DefaultNN.
        n_samples: int, optional
            The number of (parameter, simulated data) tuple to be generated to learn the summary statistics in pilot
            step. The default value is 1000.
            This is ignored if `simulations` and `parameters` are provided.
        n_samples_per_param: int, optional
            Number of data points in each simulated data set. This is ignored if `simulations` and `parameters` are
            provided. Default to 1.
        parameters: array, optional
            A numpy array with shape (n_samples, n_parameters) that is used, together with `simulations` to fit the
            summary selection learning algorithm. It has to be provided together with `simulations`, in which case no
            other simulations are performed. Default value is None.
        simulations: array, optional
            A numpy array with shape (n_samples, output_size) that is used, together with `parameters` to fit the
            summary selection learning algorithm. It has to be provided together with `parameters`, in which case no
            other simulations are performed. Default value is None.
        seed: integer, optional
            Optional initial seed for the random number generator. The default value is generated randomly.
        cuda: boolean, optional
             If cuda=None, it will select GPU if it is available. Or you can specify True to use GPU or False to use CPU
        scale_samples: boolean, optional
            If True, a scaler of the class `sklearn.preprocessing.MinMaxScaler` will be fit on the training data before 
            neural network training, and training and validation data simulations data will be rescaled. 
            When calling the `get_statistics` method, 
            a network of the class `ScalerAndNet` will be used in instantiating the statistics; this network is a 
            wrapper of a neural network and a scaler and transforms the data with the scaler before applying the neural
            network.  
            It is highly recommended to use a scaler, as neural networks are sensitive to the range of input data. A 
            case in which you may not want to use a scaler is timeseries data, as the scaler works independently on each
            feature of the data.
            Default value is True. 
        quantile: float, optional
            quantile used to define the similarity set if distance_learning is True. Default to 0.1.
        batch_size: integer, optional
            the batch size used for training the neural network. Default is 16
        n_epochs: integer, optional
            the number of epochs used for training the neural network. Default is 200
        positive_weight: float, optional
            The contrastive loss samples pairs of elements at random, and if the majority of samples are labelled as
            dissimilar, the probability of considering similar pairs is small. Then, you can set this value to a number
            between 0 and 1 in order to sample positive pairs with that probability during training.
        load_all_data_GPU: boolean, optional
            If True and if we a GPU is used, the whole dataset is loaded on the GPU before training begins; this may
            speed up training as it avoid transfer between CPU and GPU, but it is not guaranteed to do. Note that if the
            dataset is not small enough, setting this to True causes things to crash if the dataset is too large.
            Default to False, you should not rely too much on this.
        margin: float, optional
            margin defining the contrastive loss. The larger it is, the further away dissimilar samples are pushed with
            respect to similar ones. Default to 1.
        lr: float, optional
            The learning rate to be used in the iterative training scheme of the neural network. Default to 1e-3.
        optimizer: torch Optimizer class, optional
            A torch Optimizer class, for instance `SGD` or `Adam`. Default to `Adam`. Additional parameters may be
            passed through the `optimizer_kwargs` parameter.
        scheduler: torch _LRScheduler class, optional
            A torch _LRScheduler class, used to modify the learning rate across epochs. By default, no scheduler is
            used. Additional parameters may be passed through the `scheduler_kwargs` parameter.
        start_epoch_training: integer, optional
            If a scheduler is provided, for the first `start_epoch_training` epochs the scheduler is applied to modify
            the learning rate without training the network. From then on, the training proceeds normally, applying both
            the scheduler and the optimizer at each epoch. Default to 0.
        verbose: boolean, optional
            if True, prints more information from the training routine. Default to False.
        optimizer_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the optimizer.
        scheduler_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the scheduler.
        loader_kwargs: Python dictionary, optional
            dictionary containing optional keyword arguments for the loader (that handles loading the samples from the
            dataset during the training phase).
        """

        super(ContrastiveDistanceLearning, self).__init__(model, statistics_calc, backend, contrastive_training,
                                                          distance_learning=True, embedding_net=embedding_net,
                                                          n_samples=n_samples, n_samples_val=n_samples_val,
                                                          n_samples_per_param=n_samples_per_param,
                                                          parameters=parameters, simulations=simulations,
                                                          parameters_val=parameters_val,
                                                          simulations_val=simulations_val,
                                                          early_stopping=early_stopping,
                                                          epochs_early_stopping_interval=epochs_early_stopping_interval,
                                                          start_epoch_early_stopping=start_epoch_early_stopping,
                                                          seed=seed, cuda=cuda, scale_samples=scale_samples,
                                                          quantile=quantile, batch_size=batch_size, n_epochs=n_epochs,
                                                          positive_weight=positive_weight,
                                                          load_all_data_GPU=load_all_data_GPU, margin=margin, lr=lr,
                                                          optimizer=optimizer, scheduler=scheduler,
                                                          start_epoch_training=start_epoch_training,
                                                          optimizer_kwargs=optimizer_kwargs,
                                                          scheduler_kwargs=scheduler_kwargs,
                                                          loader_kwargs=loader_kwargs)
