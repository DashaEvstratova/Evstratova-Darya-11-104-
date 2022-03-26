"""
tests for hash_map
"""
import unittest
from src.hash_map import HashMap

class SampleCase(unittest.TestCase):
    """
    make the class of test
    """
    def setUp(self):
        self.hash_mapa = HashMap()

    def test_hash_map(self):
        """
        test of __getitem__ and __setitem__
        """
        self.hash_mapa["sd"] = 42
        self.assertEqual(self.hash_mapa["sd"], 42)

    def test_delkey(self):
        """
        test of delete
        """
        self.hash_mapa["sd"] = 42
        del self.hash_mapa["sd"]
        self.assertRaises(KeyError, lambda: self.hash_mapa["sd"])

    def test_size(self):
        """
        test of big size
        """
        for i in range(7):
            self.hash_mapa[i] = i
        leng1 = len(self.hash_mapa)
        self.hash_mapa[7] = 7
        leng2 = len(self.hash_mapa)
        self.assertTrue(leng1<leng2)

    def test_min_size(self):
        """
        test of min size
        """
        for i in range(4):
            self.hash_mapa[i] = i
        leng1 = len(self.hash_mapa)
        del self.hash_mapa[3]
        leng2 = len(self.hash_mapa)
        self.assertTrue(leng1>leng2)

    def test_eq_key(self):
        """
        test of __setitem__
        """
        self.hash_mapa["key"] = 1
        self.hash_mapa["key"] = 2
        self.assertEqual(self.hash_mapa["key"], 2)

if __name__=='__main__':
    unittest.main()
