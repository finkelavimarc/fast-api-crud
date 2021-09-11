from abc import ABC, abstractmethod


class Authentication(ABC):
    @abstractmethod
    def verify_password(plain_password: str, hashed_password: str):
        pass

    def get_password_hash(plain_password: str):
        pass
