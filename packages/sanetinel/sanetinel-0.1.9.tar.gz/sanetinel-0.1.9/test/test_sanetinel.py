# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.
"""
File providing unit tests for the `Sanetinel` class.
"""
import math

from unittest import TestCase
from sanetinel import sanetinel, SanetinelExperiment
from sanetinel.errors import UnknownChannelException


class TestSanetinel(TestCase):
    """
    Tests covering basic Sanetinel usage.
    """
    def test_name(self):
        """
        Tests the behaviour of the 'name' property.
        """
        self.assertEqual(sanetinel('name1').name, 'name1')
        self.assertEqual(sanetinel('name with space').name, 'name with space')

    def test_logging(self):
        """
        """
        s = sanetinel('test_logging')
        s.train()
        s.log('x', 1)
        s.log('y', 33)
        s.log('y', -2)
        with SanetinelExperiment("another"):
            s.log('y', -3)
        _expected = {
            'x': [{'channel': 'x', 'experiment': 'experiment', 'value': 1}],
            'y': [
                {'channel': 'y', 'experiment': 'experiment', 'value': 33},
                {'channel': 'y', 'experiment': 'experiment', 'value': -2},
                {'channel': 'y', 'experiment': 'another', 'value': -3}
            ]
        }
        self.assertEqual(_expected, s.dump_to_dict())

    def test_dump_load_dict(self):
        """
        Tests dumping and loading the Sanetinel data.
        """
        s = sanetinel('test_dump_load_dict')
        s.train()
        s.log('x', 1)
        s.log('x', 100)
        s.log('y', 33)
        s.log('y', -2)

        data = s.dump_to_dict()
        xbar = s.mean('x')
        ybar = s.mean('y')
        xstd = s.std('x')
        ystd = s.std('y')

        s = sanetinel('test2')
        s.load_from_dict(data)
        self.assertEqual(s.name, 'test2')
        self.assertAlmostEqual(s.mean('x'), xbar)
        self.assertAlmostEqual(s.mean('y'), ybar)
        self.assertAlmostEqual(s.std('x'), xstd)
        self.assertAlmostEqual(s.std('y'), ystd)

    def test_mean_stddev(self):
        """
        Tests computing mean and standard deviation.
        """
        s = sanetinel('test_mean_stddev')
        s.train()
        s.log('x', 1)
        s.log('x', 40)
        s.log('x', 100)
        s.log('y', 33)
        s.log('y', -2)

        xbar = (1 + 40 + 100) / 3.0
        ybar = (33 - 2) / 2.0

        self.assertAlmostEqual(s.mean('x'), xbar)
        self.assertAlmostEqual(s.mean('y'), ybar)

        # Working with Sample variance here
        xstd = (sum([(1 - xbar)**2, (40 - xbar)**2, (100 - xbar)**2]) / (2.0)) ** 0.5
        ystd = (sum([(33 - ybar)**2, (-2 - ybar)**2]) / 1.0) ** 0.5

        self.assertAlmostEqual(s.std('x'), xstd)
        self.assertAlmostEqual(s.std('y'), ystd)

        # Values should not be impacted by testing
        s.test()
        s.log('x', 70)

        self.assertAlmostEqual(s.mean('x'), xbar)
        self.assertAlmostEqual(s.mean('y'), ybar)
        self.assertAlmostEqual(s.std('x'), xstd)
        self.assertAlmostEqual(s.std('y'), ystd)

    def test_return_values(self):
        s = sanetinel("test_return_values")
        s.train()
        s.log('x', 5)
        s.log('x', 6)
        s.log('x', 7)
        s.log('y', 1)

        s.test()
        self.assertEqual(s.log('x', 4), 2.0)
        self.assertEqual(s.log('y', 1), 0)
        self.assertEqual(s.log('y', 2), math.inf)
        with self.assertRaises(UnknownChannelException):
            self.assertEqual(s.log('z', 1), math.inf)
