'''
do the hash_map
'''

from dataclasses import dataclass
from src.maps.base_map import BaseMap
class HashMap(BaseMap):
    """
    to do class HashMap
    """
    @dataclass
    class Node:
        """
        to do class Node
        """
        next = None
        def __init__(self, value = None, key = None):
            self.key = key
            self.value = value

        def __iter__(self):
            yield self.key, self.value

            if self.next is not None:
                yield from self.next

    @dataclass
    class Innerlinkedlist:
        """
        to do class LinkedList
        """
        head = None
        end = None
        length = 0

        def insertatend(self, value, key):
            """
            method insertatend
            """
            if self.head is None:
                self.head = self.end = HashMap.Node(value, key)
            else:
                self.end.next = self.end = HashMap.Node(value, key)
            self.length +=1

        def deletkey(self, key):
            """
            method delet
            """
            node = self.head
            leng = self.length
            if node.key == key:
                self.head = node.next
                self.length-=1
            else:
                while node.next:
                    if node.next.key == key:
                        node.next = node.next.next
                        self.length -= 1
                        break
            if leng == self.length:
                raise KeyError("Нет элемента с таким ключом")

        def __len__(self):
            return self.length

        def __iter__(self):
            if self.head is not None:
                yield from self.head

    def __init__(self, _size=10):
        self._inner_list = [None] *_size
        self._size = _size
        self._leng = 0

    def __getitem__(self, key):
        linked_list = self._inner_list[hash(key) % self._size]
        if linked_list is None:
            return None
        node = linked_list.head
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def __setitem__(self, key, value):
        hash_key = hash(key) % self._size
        if self._inner_list[hash_key] is None:
            self._inner_list[hash_key] = HashMap.Innerlinkedlist()
            self._inner_list[hash_key].insertatend(value, key)
        else:
            node = self._inner_list[hash_key]
            prev_node = node.head
            while prev_node:
                if prev_node.key == key:
                    prev_node.value = value
                    return
                prev_node = prev_node.next
            node.insertatend(value, key)
        self._leng += 1
        if self._leng >= (0.8 * self._size):
            self._size *=2
            new_list = [None] *self._size
            for elem_node in self._inner_list:
                if elem_node:
                    node = elem_node.head
                    set(node, new_list, key, value)
            self._inner_list = new_list

    def set(self, node, new_list, key, value):
        """
        helping method __setitem__
        """
        while node:
            hash_key = hash(node.key) % self._size
            if new_list[hash_key] is None:
                new_list[hash_key] = HashMap.Innerlinkedlist()
                new_list[hash_key].insertatend(node.value, node.key)
            else:
                prev_node = new_list[hash_key]
                pr_prev = prev_node.head
                while pr_prev:
                    if pr_prev.key == key:
                        pr_prev.value = value
                        return
                    pr_prev = pr_prev.next
                prev_node.insertatend(value, key)
            node = node.next

    def __delitem__(self, key):
        for elem_node in self._inner_list:
            if elem_node:
                if len(elem_node)>0:
                    elem_node.deletkey(key)
                else:
                    raise KeyError("Нет элемента с таким ключом")
        self._leng -=1
        if self._leng < self._size * 0.35 and self._size >0:
            self._size = self._size//2
            new_list = [None] * self._size
            for elem_node in self._inner_list:
                if elem_node:
                    node = elem_node.head
                    while node:
                        hash_key = hash(node.key) % self._size
                        if new_list[hash_key] is None:
                            new_list[hash_key] = HashMap.Innerlinkedlist()
                            new_list[hash_key].insertatend(node.value, node.key)
                        else:
                            list_n = new_list[hash_key]
                            list_n.insertatend(node.value, node.key)
                        node = node.next
            self._inner_list = new_list

    def __len__(self):
        return self._leng

    def __iter__(self):
        for inner in self._inner_list:
            yield from inner or []
