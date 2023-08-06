# --- Task and types definitions

import unittest

from datamaestro.test import DatasetTests
from datamaestro import Context


class MainTest(DatasetTests, unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
