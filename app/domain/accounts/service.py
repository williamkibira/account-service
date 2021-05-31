from app.core.security.password_handler import PasswordHandler
from app.core.storage.storage import FileStorage
from app.domain.accounts.accounts_pb2 import RegistrationDetails, UpdateDetails
from app.domain.acm.users.repository import UserRepository


class AccountService:
    def __init__(self, file_storage: FileStorage, user_repository: UserRepository, password_handler: PasswordHandler):
        self.__file_storage: FileStorage = file_storage
        self.__user_repository: UserRepository = user_repository
        self.__password_handler: PasswordHandler = password_handler
        pass

    def register(self, details: RegistrationDetails) -> str:
        pass

    def update(self, details: UpdateDetails) -> None:
        pass
