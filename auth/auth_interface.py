from abc import ABC, abstractmethod


class Authentication(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str):
        pass

    @staticmethod
    @abstractmethod
    def get_password_hash(plain_password: str):
        pass
