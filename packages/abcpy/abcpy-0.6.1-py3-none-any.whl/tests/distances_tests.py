import unittest

import numpy as np

from abcpy.distances import Euclidean, PenLogReg, LogReg, Wasserstein
from abcpy.statistics import Identity


class EuclideanTests(unittest.TestCase):
    def setUp(self):
        self.stat_calc = Identity(degree=1, cross=0)
        self.distancefunc = Euclidean(self.stat_calc)

    def test_distance(self):
        # test simple distance computation
        a = [[0, 0, 0], [0, 0, 0]]
        b = [[0, 0, 0], [0, 0, 0]]
        c = [[1, 1, 1], [1, 1, 1]]
        # Checks whether wrong input type produces error message
        self.assertRaises(TypeError, self.distancefunc.distance, 3.4, b)
        self.assertRaises(TypeError, self.distancefunc.distance, a, 3.4)

        # test input has different dimensionality
        self.assertRaises(BaseException, self.distancefunc.distance, a, np.array([[0, 0], [1, 2]]))
        self.assertRaises(BaseException, self.distancefunc.distance, a, np.array([[0, 0, 0], [1, 2, 3], [4, 5, 6]]))

        # test whether they compute correct values
        self.assertTrue(self.distancefunc.distance(a, b) == np.array([0]))
        self.assertTrue(self.distancefunc.distance(a, c) == np.array([1.7320508075688772]))

    def test_dist_max(self):
        self.assertTrue(self.distancefunc.dist_max() == np.inf)


class PenLogRegTests(unittest.TestCase):
    def setUp(self):
        self.stat_calc = Identity(degree=1, cross=False)
        self.distancefunc = PenLogReg(self.stat_calc)
        self.rng = np.random.RandomState(1)

    def test_distance(self):
        d1 = 0.5 * self.rng.randn(100, 2) - 10
        d2 = 0.5 * self.rng.randn(100, 2) + 10
        d3 = 0.5 * self.rng.randn(95, 2) + 10

        d1 = d1.tolist()
        d2 = d2.tolist()
        d3 = d3.tolist()
        # Checks whether wrong input type produces error message
        self.assertRaises(TypeError, self.distancefunc.distance, 3.4, d2)
        self.assertRaises(TypeError, self.distancefunc.distance, d1, 3.4)

        # completely separable datasets should have a distance of 1.0
        self.assertEqual(self.distancefunc.distance(d1, d2), 1.0)

        # equal data sets should have a distance of 0.0
        self.assertEqual(self.distancefunc.distance(d1, d1), 0.0)

        # equal data sets should have a distance of 0.0; check that in case where n_samples is not a multiple of n_folds
        # in cross validation (10)
        self.assertEqual(self.distancefunc.distance(d3, d3), 0.0)

        # check if it returns the correct error when the number of datasets:
        self.assertRaises(RuntimeError, self.distancefunc.distance, d1, d3)

    def test_dist_max(self):
        self.assertTrue(self.distancefunc.dist_max() == 1.0)


class LogRegTests(unittest.TestCase):
    def setUp(self):
        self.stat_calc = Identity(degree=2, cross=False)
        self.distancefunc = LogReg(self.stat_calc, seed=1)
        self.rng = np.random.RandomState(1)

    def test_distance(self):
        d1 = 0.5 * self.rng.randn(100, 2) - 10
        d2 = 0.5 * self.rng.randn(100, 2) + 10

        d1 = d1.tolist()
        d2 = d2.tolist()

        # Checks whether wrong input type produces error message
        self.assertRaises(TypeError, self.distancefunc.distance, 3.4, d2)
        self.assertRaises(TypeError, self.distancefunc.distance, d1, 3.4)

        # completely separable datasets should have a distance of 1.0
        self.assertEqual(self.distancefunc.distance(d1, d2), 1.0)

        # equal data sets should have a distance of 0.0
        self.assertEqual(self.distancefunc.distance(d1, d1), 0.0)

    def test_dist_max(self):
        self.assertTrue(self.distancefunc.dist_max() == 1.0)


class WassersteinTests(unittest.TestCase):
    def setUp(self):
        self.stat_calc = Identity(degree=2, cross=False)
        self.distancefunc = Wasserstein(self.stat_calc)
        self.rng = np.random.RandomState(1)

    def test_distance(self):
        d1 = 0.5 * self.rng.randn(100, 2) - 10
        d2 = 0.5 * self.rng.randn(100, 2) + 10

        d1 = d1.tolist()
        d2 = d2.tolist()

        # Checks whether wrong input type produces error message
        self.assertRaises(TypeError, self.distancefunc.distance, 3.4, d2)
        self.assertRaises(TypeError, self.distancefunc.distance, d1, 3.4)

        # completely separable datasets should have a distance of 1.0
        self.assertEqual(self.distancefunc.distance(d1, d2), 28.623685155319652)

        # equal data sets should have a distance of approximately 0.0; it won't be exactly 0 due to numerical rounding
        self.assertAlmostEqual(self.distancefunc.distance(d1, d1), 0.0, delta=1e-5)

    def test_dist_max(self):
        self.assertTrue(self.distancefunc.dist_max() == np.inf)


if __name__ == '__main__':
    unittest.main()
