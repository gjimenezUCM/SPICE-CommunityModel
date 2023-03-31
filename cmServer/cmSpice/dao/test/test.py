# file 2: test_other.py, put this under same directory
import unittest
import test_api
import test_file
from context import dao

suite = unittest.TestLoader().loadTestsFromModule(test_api)
suite = unittest.TestLoader().discover("")


unittest.TextTestRunner(verbosity=2).run(suite)