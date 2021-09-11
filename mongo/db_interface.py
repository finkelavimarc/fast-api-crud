from typing import AbstractSet
from abc import ABC, abstractmethod


class CrudOperations(ABC):
    @abstractmethod
    def find_one(filter: dict):
        pass

    @abstractmethod
    def insert(element: dict):
        pass
