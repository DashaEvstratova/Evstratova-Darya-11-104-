import unittest
from scr1.TreeMap import TreeMap

class SampleCase(unittest.TestCase):

    def setUp(self): # Запускается при каждом тесте
        self.hm = TreeMap()

    def test_tree_map(self): # Проверка работы фунции __getitem__
        self.hm[4] = 42 # Добавление элемента в массив
        self.assertEquals(self.hm[4], 42) # Проверка является ключ 4 к значению 42
    def test_doubl_key(self):
        self.hm[4] = 42
        self.hm[4] = 67
        self.assertEquals(self.hm[4], 67)
if __name__=='__main__':
    unittest.main()