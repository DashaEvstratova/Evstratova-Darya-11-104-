class HashMap:
    class Node: # Класс узла
        def __init__(self,value = None,key = None ):
            self.value = value
            self.key = key
            self.next = None

    class Innerlinkedlist: # Класс односвязного списка
        def __init__(self):
            self.head = None
            self.end = None
            self.length = 0

        def insertatend(self,value, key): # Вставка в конец
            if self.head is None: # Если односвязного списка нет
                self.head = self.end = HashMap.Node(value, key)
            else: # Если есть, то поставить его перед концом, None
                self.end.next = self.end = HashMap.Node(value, key)
            self.length +=1

        def deletkey(self, key): # Удаление элемента из списка по ключу
            a = self.head
            if a.key == key: # Если такой ключ первый, то заменить его на след.
                self.head = a.next
                self.length-=1
            else: # В противном идем по списку, когда находим убираем его и сдвигаем
                while a.next:
                    if a.next.key == key:
                        a.next = a.next.next
                        self.length -=1
                        return
            return KeyError("Нет элемента с таким ключом")

        def __len__(self):
            return self.length

    def __init__(self, _size=10):
        self._inner_list = [None] *_size
        self._size = _size
        self._leng = 0

    def __getitem__(self, key): # Получение элемента по ключу
        linked_list = self._inner_list[hash(key) % self._size]
        if linked_list is None: # Если такого хэша еще не было, то создается список для него
            raise KeyError("Нет элемента с таким ключом")
        a = linked_list.head # В противном же случае проходимся по списку с таким же значением хеша
        while a:
            if a.key == key:
                return a.value
            a = a.next
        raise KeyError("Нет элемента с таким ключом")

    def __setitem__(self, key, value): # Настройка элементов
        x = hash(key) % self._size # Получение хеша для элемента
        if self._inner_list[x] is None: # Если по такому хэшу не создано списка
            self._inner_list[x] = HashMap.Innerlinkedlist() # Создание списка
            self._inner_list[x].insertatend(value, key) # Добавление элемента в этот список
        else: # В противном случае проходимся по существуемому списку
            a = self._inner_list[x]
            b = a.head
            while b:
                if b.key == key: # Если такой ключ уже есть, то заменить значение
                    b.value = value
                    return
                b = b.next
            a.insertatend(value, key) # Если не найден такой ключ, то добавить узел с этим значением и ключом
        self._leng += 1
        if self._leng >= (0.8 * self._size): # Если массив заполнен на 80%, то увеличить вдвое
            self._size *=2
            new_list = [None] *self._size # Новый массив, вдвое больше
            for el in self._inner_list: # Проход по всем спискам
                if el: # Проверка, что список не пустой
                    a = el.head
                    while a: # Проход по списку
                        x = hash(a.key) % self._size
                        if new_list[x] is None: # Если еще нет списка с таким значением хеша, то создаем
                            new_list[x] = HashMap.Innerlinkedlist()
                            new_list[x].insertatend(a.value, a.key)
                        else: # В противном случае, проходимся по списку, и записываем значенмя в новый список
                            b = new_list[x]
                            c = b.head
                            while c:
                                if c.key == key:
                                    c.value = value
                                    return
                                c = c.next
                            b.insertatend(value, key)
                        a = a.next
            self._inner_list = new_list # Перезаписываем новый в переменную старого списка

    def __delitem__(self, key): # Удаление элемента из массива по ключу и его уменьшение
        for el in self._inner_list: # Проход по массиву
            if el: # Если элемент массива не пустой
                if len(el)>0: # Проверка длины списка на месте этого элемента
                    el.deletkey(key) # Если есть список, то удаляем по ключу элемент
                else:
                    return KeyError("Нет элемента с таким ключом")
        self._leng -=1
        if self._leng < self._size * 0.35 and self._size >0:
            self._size = self._size//2
            new_list = [None] * self._size  # Новый массив, вдвое больше
            for el in self._inner_list:  # Проход по всем спискам
                if el:  # Проверка, что список не пустой
                    a = el.head
                    while a:  # Проход по списку
                        x = hash(a.key) % self._size
                        if new_list[x] is None:  # Если еще нет списка с таким значением хеша, то создаем
                            new_list[x] = HashMap.Innerlinkedlist()
                            new_list[x].insertatend(a.value, a.key)
                        else:  # В противном случае, на место элемента добавляем список с элемнтами
                            b = new_list[x]
                            b.insertatend(a.value, a.key)
                        a = a.next
            self._inner_list = new_list  # Перезаписываем новый в переменную старого списка

    def __len__(self):
        return self._size
