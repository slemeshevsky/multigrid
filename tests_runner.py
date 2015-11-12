#!/usr/bin/env python

import unittest
from mg.smoother import *
import numpy as np

loader = unittest.TestLoader()
suite = loader.discover(start_dir='./tests', pattern="test_*.py")

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
