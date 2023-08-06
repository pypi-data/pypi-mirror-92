# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.
"""
Sanetinel
=========

Sanetinel is a simple sanity-check system for monitoring your algorithms.

.. code-block:: python
    s = sanetinel('algorithm')
    s.train()
    s.log('variable', 1)
    s.log('variable', 2)
    s.log('variable', 3)
    s.test()
    s.log('variable', 100)
"""
from .impl import sanetinel
from .types import Sanetinel
from .sanetinel_experiment import SanetinelExperiment
