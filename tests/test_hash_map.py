import unittest

from src.hash_map import HashMap

class SampleCase(unittest.TestCase):

    def setUp(self): # Запускается при каждом тесте
        self.hm = HashMap()

    def test_hash_map(self): # Проверка работы фунции __getitem__
        self.hm["sd"] = 42 # Добавление элемента в массив
        self.assertEquals(self.hm["sd"], 42) # Проверка является ключ "sd" к значению 42

    def test_delkey(self): # Проверка работы фунции delete
        self.hm["sd"] = 42 # Добавление элемента в массив
        del self.hm["sd"] # Убаление элемента
        self.assertRaises(KeyError, lambda: self.hm["sd"]) # Проверка на то, что при вызыве не существующего ключа, будет поднято исключение

    def test_size(self): # Проверка того, что массив увеличится
        for i in range(7): # Заполняем 70% массива
            self.hm[i] = i
        leng1 = len(self.hm) # Длина до изменения размера
        self.hm[7] = 7 # Массив заполнен на 80%
        leng2 = len(self.hm) # Длина после изменения
        self.assertTrue(leng1<leng2) # Проверка на то, что размер до меньше, чем после

    def test_min_size(self):# Проверка того, что массив уменьшится
        for i in range(4): # Заполняем 40% массива
            self.hm[i] = i
        leng1 = len(self.hm)# Длина до изменения размера
        del self.hm[3]# Массив заполнен на 30%
        leng2 = len(self.hm)# Длина после изменения
        self.assertTrue(leng1>leng2)# Проверка на то, что размер до больше, чем после

    def test_eq_key(self): # Проверка на то, что значение по ключу заменяется при повторе
        self.hm["key"] = 1
        self.hm["key"] = 2
        self.assertEquals(self.hm["key"], 2) # Проверка на то, что по ключу "key" будет последнее значение 2

if __name__=='__main__':
    unittest.main()