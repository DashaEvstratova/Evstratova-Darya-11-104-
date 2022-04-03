"""
Abstract class
"""
from abc import ABC, abstractmethod
from typing import Iterable, Tuple, List

class BaseMap(ABC):
    """
    general class
    """
    @abstractmethod
    def __setitem__(self, key, value) -> None:
        """
        method __setitem__
        """
    @abstractmethod
    def __getitem__(self, item) -> int:
        """
        method __getitem__
        """
    @abstractmethod
    def __delitem__(self, key) -> None:
        """
        method __delitem__
        """
    @abstractmethod
    def __len__(self) -> int:
        """
        method __len__
        """
    @abstractmethod
    def __iter__(self) -> Iterable[Tuple[str, int]]:
        """
        method __iter__
        """
    def write(self, path:str) -> None:
        """
        method write
        """
        with open(path, 'w') as w_f:
            for key, value in self:
                w_f.write(str(key) + " " + str(value) + "\n")
    @classmethod
    def read(cls, path:str) -> 'BaseMap':
        """
        method read
        """
        my_obj = cls()
        with open(path, 'r') as open_file:
            string_words = open_file.readline()
            while string_words:
                node = string_words.split()
                my_obj[node[0]] = int(node[1])
                string_words = open_file.readline()
            open_file.close()

