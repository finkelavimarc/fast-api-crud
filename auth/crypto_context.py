from passlib.context import CryptContext
from auth.auth_interface import Authentication

class CryptoContext(Authentication):
    """
    Class for handling cryptographic operations such as password hashing and verification.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify the provided plain password against the hashed password.

        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hash for the provided password.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)
