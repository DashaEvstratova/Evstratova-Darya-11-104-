"""
Abstract class
"""
from abc import ABC, abstractmethod
from typing import Iterable, Tuple
from typing import Any


class BaseMap(ABC):
    '''Abstract class for Maps'''

    @abstractmethod
    def __setitem__(self, key, value) -> None:
        pass

    @abstractmethod
    def __getitem__(self, item) -> int:
        pass

    @abstractmethod
    def __delitem__(self, key) -> None:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __iter__(self) -> Iterable[Tuple[str, int]]:
        pass

    def __contains__(self, key: str) -> bool:
        '''A method to check'''
        for data_key, _ in self:
            if data_key == key:
                return True
        return False

    def __eq__(self, other) -> bool:
        lst_self = sorted(list(self))
        lst_other = sorted(list(other))
        if lst_self == lst_other:
            return True
        return False

    def __bool__(self) -> bool:
        return len(self) != 0

    def items(self) -> Iterable[Tuple[str, int]]:
        '''D.items() -> a set-like object providing a view on D's items'''
        yield from self

    def values(self) -> Iterable[int]:
        '''D.values() -> an object providing a view on D's values'''
        return (item[1] for item in self)

    def keys(self) -> Iterable[str]:
        '''D.keys() -> a set-like object providing a view on D's keys'''
        return (item[0] for item in self)

    @classmethod
    def fromkeys(cls, iterable, value=None) -> 'BaseMap':
        '''Create a new dictionary with keys from iterable and values set to value.'''
        new_map = cls()
        for key in iterable:
            new_map[key] = value
        return new_map

    def update(self, other=None) -> None:
        '''Update D from dict/iterable E and F'''
        try:
            all_keys = other.keys()
            for key in all_keys:
                self[key] = other[key]
        except AttributeError:
            if other is not None:
                for key, value in other:
                    self[key] = value

    def get(self, key: str, default=None) -> Any:
        '''Return the value for key if key is in the dictionary, else default.'''
        if key in self:
            return self[key]
        return default

    def pop(self, key: str, default=None) -> Any:
        '''remove specified key and return the corresponding value.'''
        if key in self:
            value = self[key]
            del self[key]
            return value
        if default:
            return default
        raise KeyError

    def popitem(self) -> Tuple[str, int]:
        '''Remove and return a (key, value) pair as a 2-tuple.'''
        if self:
            inner_map = list(self)
            del self[inner_map[-1][0]]
            return inner_map[-1][0], inner_map[-1][1]
        raise KeyError

    def setdefault(self, key: str, default=None) -> int:
        ''' Insert key with a value of default if key is not in the dictionary.'''
        if key in self:
            return self[key]
        self[key] = default
        return default

    def write(self, path:str) -> None:
        '''method write'''
        with open(path, 'w', encoding='utf8') as w_f:
            for key, value in self:
                w_f.write(str(key) + " " + str(value) + "\n")

    @classmethod
    def read(cls, path:str) -> 'BaseMap':
        '''method read'''
        my_obj = cls()
        with open(path, 'r', encoding='utf8') as open_file:
            string_words = open_file.readline()
            while string_words:
                node = string_words.split()
                my_obj[node[0]] = int(node[1])
                string_words = open_file.readline()
            open_file.close()
