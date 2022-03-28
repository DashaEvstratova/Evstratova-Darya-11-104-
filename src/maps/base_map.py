"""
Abstract class
"""
from abc import ABC, abstractmethod
from typing import Iterable, Tuple, List
from os import path

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
        for key, value in self:
            pass
    @classmethod
    def read(cls, path:str) -> 'BasMap':
        """
        method read
        """
        my_obj = cls()
        open_file = ...
        for key, value in open_file:
            my_obj[key] = value
        return my_obj