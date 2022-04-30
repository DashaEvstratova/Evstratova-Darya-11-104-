"""
testing MappingProtocol
"""
import unittest
from test import mapping_tests

from src.maps.hash_map import HashMap


class GeneralMappingTests(mapping_tests.BasicTestMappingProtocol):
    """
    mocked test_read
    """
    type2test = HashMap

    def test_read(self):
        # Test for read only operations on mapping
        objecty = self._empty_mapping()
        objecty1 = dict(objecty) #workaround for singleton objects
        diction = self._full_mapping(self.reference)
        if diction is objecty:
            objecty = objecty1
        #Indexing
        for key, value in self.reference.items():
            self.assertEqual(diction[key], value)
        knownkey = list(self.other.keys())[0]
        self.assertRaises(KeyError, lambda:diction[knownkey])
        #len
        self.assertEqual(len(objecty), 0)
        self.assertEqual(len(diction), len(self.reference))
        #__contains__
        for k in self.reference:
            self.assertIn(k, diction)
        for k in self.other:
            self.assertNotIn(k, diction)
        #cmp
        self.assertEqual(objecty, objecty)
        self.assertEqual(diction, diction)
        self.assertNotEqual(objecty, diction)
        self.assertNotEqual(diction, objecty)
        #bool
        if objecty:
            self.fail("Empty mapping must compare to False")
        if not diction:
            self.fail("Full mapping must compare to True")
        # keys(), items(), iterkeys() ...
        def check_iterandlist(iter, lst, ref):
            self.assertTrue(hasattr(iter, '__next__'))
            self.assertTrue(hasattr(iter, '__iter__'))
            lst = list(iter)
            self.assertTrue(set(lst) == set(lst) == set(ref))
        check_iterandlist(iter(diction.keys()), list(diction.keys()),
                          self.reference.keys())
        check_iterandlist(iter(diction.keys()), list(diction.keys()), self.reference.keys())
        check_iterandlist(iter(diction.values()), list(diction.values()),
                          self.reference.values())
        check_iterandlist(iter(diction.items()), list(diction.items()),
                          self.reference.items())
        #get
        key, value = next(iter(diction.items()))
        knownkey, knownvalue = next(iter(self.other.items()))
        self.assertEqual(diction.get(key, knownvalue), value)
        self.assertEqual(diction.get(knownkey, knownvalue), knownvalue)
        self.assertNotIn(knownkey, diction)


if __name__ == "__main__":
    unittest.main()
