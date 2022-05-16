'''
do the hash_map
'''

from typing import Iterable, Tuple
from src.maps.base_map import BaseMap


class HashMap(BaseMap):
    '''Class HashMap'''

    class Node:
        '''class of Node'''
        def __init__(self, value: int, key: str, next_node=None) -> None:
            self.value = value
            self.key = key
            self.next = next_node

        def __iter__(self) -> Iterable[Tuple[str, int]]:
            yield self.key, self.value

            if self.next is not None:
                yield from self.next

        def __str__(self) -> str:
            return f"key: {self.key}, value: {self.value}"

    class LinkedList:
        '''class LinkedList'''
        def __init__(self) -> None:
            self.head = None
            self.end = None
            self.length = 0

        def insert_end(self, value, key):
            '''add method to singly linked list'''
            if self.head is None:
                self.head = self.end = HashMap.Node(value, key)
            else:
                self.end.next = self.end = HashMap.Node(value, key)
            self.length += 1

        def delete_key(self, key):
            '''remove method to singly linked list'''
            current = self.head
            if self.head is None:
                return
            if self.head.key == key:
                self.head = self.head.next
            else:
                while current.next is not None:
                    if current.next.key == key:
                        current.next = current.next.next
                        self.length -= 1
                        break

        def __len__(self) -> int:
            return self.length

        def __str__(self) -> str:
            if self.head is not None:
                current = self.head
                result = f'[{current.value}, '
                while current.next is not None:
                    current = current.next
                    result += f'{current.value}, '
                result = result[:-2]
                result += ']'
                return result
            return '[]'

        def __iter__(self) -> Iterable[Tuple[str, int]]:
            if self.head is not None:
                yield from self.head

    def __init__(self, size=10) -> None:
        self._inner_list = [None] * size
        self._size = size
        self._cnt = 0

    def __iter__(self) -> Iterable[Tuple[str, int]]:
        for linklist in self._inner_list:
            yield from linklist or []

    def __getitem__(self, key: str) -> int:
        linklist = self._inner_list[hash(key) % self._size]
        if linklist is None:
            raise KeyError
        current = linklist.head
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError

    def __setitem__(self, key: str, value: int) -> None:
        index = hash(key) % self._size
        if self._inner_list[index] is None:
            self._inner_list[index] = HashMap.LinkedList()
            self._inner_list[index].insert_end(value, key)
        else:
            lst = self._inner_list[index]
            current = lst.head
            while current is not None:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            lst.insert_end(value, key)
        self._cnt += 1
        if self._cnt >= 0.8 * self._size:
            self._size = self._size * 17 // 10
            new_inner_list = [None] * self._size
            for linlist in self._inner_list:
                if linlist is not None:
                    current = linlist.head
                    while current is not None:
                        index = hash(current.key) % self._size
                        if new_inner_list[index] is None:
                            new_inner_list[index] = HashMap.LinkedList()
                            new_inner_list[index].insert_end(current.value, current.key)
                        else:
                            lst = new_inner_list[index]
                            lst.insert_end(current.key, current.value)
                        current = current.next
            self._inner_list = new_inner_list

    def __delitem__(self, key: str) -> None:
        for linklist in self._inner_list:
            if linklist is not None:
                linklist.delete_key(key)
        self._cnt -= 1
        if self._size * 0.8 > self._cnt and self._size > 10:
            self._size = self._size // 17 * 10  # decreasing by 2
            new_inner_list = [None] * self._size
            for linlist in self._inner_list:
                if linlist is not None:
                    current = linlist.head
                    while current is not None:
                        index = hash(current.key) % self._size
                        if new_inner_list[index] is None:
                            new_inner_list[index] = HashMap.LinkedList()
                            new_inner_list[index].insert_end(current.value, current.key)
                        else:
                            lst = new_inner_list[index]
                            lst.insert_end(current.value, current.key)
                        current = current.next
            self._inner_list = new_inner_list

    def __contains__(self, item):
        for linlist in self._inner_list:
            if linlist is not None:
                for elem in linlist:
                    if elem[0] == item:
                        return True
        return False

    def __len__(self) -> int:
        return self._cnt

    def __str__(self) -> str:
        return '[' + ', '.join(map(str, self._inner_list)) + ']'

    def clear(self) -> None:
        """clear"""
        self._size = 10
        self._inner_list = [None] * self._size
        self._cnt = 0
