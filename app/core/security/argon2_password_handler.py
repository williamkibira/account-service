from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError

from app.core.security.password_handler import PasswordHandler


class Configuration(object):
    def __init__(self):
        self.type: Type = None
        self.memory_cost: int = None
        self.salt_length: int = None
        self.hash_length: int = None
        self.parallelism: int = None
        self.time_cost: int = None


class Argon2PasswordHandler(PasswordHandler):

    def __init__(self, configuration: Configuration) -> None:
        self.__hasher: PasswordHasher = PasswordHasher(
            time_cost=configuration.time_cost,
            parallelism=configuration.parallelism,
            hash_len=configuration.hash_length,
            salt_len=configuration.salt_length,
            memory_cost=configuration.memory_cost,
            type=configuration.type
        )

    def hash(self, password: str) -> str:
        return self.__hasher.hash(password=password)

    def verify(self, input_password: str, existing_hash: str) -> bool:
        try:
            return self.__hasher.verify(hash=existing_hash, password=input_password)
        except VerifyMismatchError as error:
            print("ERROR: {}".format(error))
            return False
