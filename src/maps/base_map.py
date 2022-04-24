"""
Abstract class
"""
from abc import ABC, abstractmethod
from typing import Iterable, Tuple

class BaseMap(ABC):

    """general class"""
    @abstractmethod
    def __setitem__(self, key, value) -> None:
        """method __setitem__"""

    @abstractmethod
    def __getitem__(self, item) -> int:
        """method __getitem__"""

    @abstractmethod
    def __delitem__(self, key) -> None:
        """method __delitem__"""

    @abstractmethod
    def __len__(self) -> int:
        """method __len__"""

    @abstractmethod
    def __iter__(self) -> Iterable[Tuple[str, int]]:
        """method __iter__"""

    def __contains__(self, key: str) -> bool:
        """method __contains__"""

    def __eq__(self, other: 'BaseMap') -> bool:
        """method __eq__"""
        if self.__len__() != other.__len__():
            return False
        for element in self:
            if not other.__contains__(element[0]):
                return False
            if other[element[0]] != element[1]:
                return False
        return True

    def __bool__(self) -> bool:
        """method __bool__"""
        if len(self) == 0:
            return False
        return True

    def items(self) -> Iterable[Tuple[str, int]]:
        """method items"""
        yield from self

    def values(self) -> Iterable[int]:
        """method values"""
        return (item[1] for item in self)

    def keys(self) -> Iterable[str]:
        """method keys"""
        return (item[0] for item in self)

    @classmethod
    def fromkeys(cls, iterable, value=None) -> 'BaseMap':
        """fromkeys"""
        my_class = cls()
        for key in iterable:
            my_class[key] = value
        return iterable

    def update(self, other=None) -> None:
        """update"""
        if other is not None:
            if hasattr(other, 'keys'):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value

    def get(self, key, default=None):
        """get"""
        if self[key]:
            return self[key]
        return default

    def pop(self, key, *args):
        """pop"""
        if self[key]:
            node = self[key]
            self.__delitem__(key)
            return node
        if args:
            return args[0]
        raise KeyError

    def popitem(self):
        """popitem"""
        if not self.__bool__:
            for element in self:
                last = element
            self.__delitem__(last)
            return (last, self[last])
        raise KeyError

    def setdefault(self, key, default=None):
        """setdefault"""
        for element in self:
            if element[0] == key:
                return element[1]
        self[key] = default
        return default

    def clear(self):
        """clear"""
        for key, _ in self:
            self.__delitem__(key)
        return self

    def write(self, path:str) -> None:
        """method write"""
        with open(path, 'w', encoding='utf8') as w_f:
            for key, value in self:
                w_f.write(str(key) + " " + str(value) + "\n")

    @classmethod
    def read(cls, path:str) -> 'BaseMap':
        """method read"""
        my_obj = cls()
        with open(path, 'r', encoding='utf8') as open_file:
            string_words = open_file.readline()
            while string_words:
                node = string_words.split()
                my_obj[node[0]] = int(node[1])
                string_words = open_file.readline()
            open_file.close()
