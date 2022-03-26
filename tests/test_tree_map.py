"""
tests for tree_map
"""

import unittest
from src.tree_map import TreeMap

class SampleCase(unittest.TestCase):
    """
    make the class of test
    """
    def setUp(self): # Запускается при каждом тесте
        self.treemap = TreeMap()

    def test_tree_map(self):
        """
        test of __getitem__
        """
        self.treemap[4] = 42
        self.assertEqual(self.treemap[4], 42)

    def test_doubl_key(self):
        """
        test of __setitem__
        """
        self.treemap[4] = 42
        self.treemap[4] = 67
        self.assertEqual(self.treemap[4], 67)

if __name__=='__main__':
    unittest.main()
