from abc import ABC, abstractmethod
from typing import Iterable, Tuple, List
from os import path

class BasMap(ABC):
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
    def write(self, path:str) -> None:
        for key, value in self:
            pass
    @classmethod
    def read(cls, path:str) -> 'BasMap':
        my_obj = cls()
        open_file = ...
        for key, value in open_file:
            my_obj[key] = value
        return my_obj