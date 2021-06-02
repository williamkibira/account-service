import uuid
from typing import Dict

import falcon

from app.core.security.password_handler import PasswordHandler
from app.core.storage.storage import FileStorage
from app.domain.accounts.accounts_pb2 import RegistrationDetails, UpdateDetails
from app.domain.acm.users.models import User
from app.domain.acm.users.repository import UserRepository


class AccountService:
    def __init__(self, file_storage: FileStorage, user_repository: UserRepository, password_handler: PasswordHandler):
        self.__file_storage: FileStorage = file_storage
        self.__user_repository: UserRepository = user_repository
        self.__password_handler: PasswordHandler = password_handler
        pass

    def register(self, details: RegistrationDetails) -> str:
        identifier = str(uuid.uuid4())
        hashed_password: str = self.__password_handler.hash(password=details.password)
        photo_identifier: str = self.__save_photo(content=details.photo, content_type=details.photo_content_type)
        self.__user_repository.save(
            user=User(
                identifier=identifier,
                first_name=details.first_name,
                last_name=details.last_name,
                email_address=details.email,
                password=hashed_password,
                photo_identifier=photo_identifier
            ),
            roles=details.roles
        )
        return identifier

    def update(self, identifier: str, details: UpdateDetails) -> None:
        changes: Dict[str] = {
            'first_name': details.first_name,
            'last_name': details.last_name,
            'email_address': details.email
        }
        if len(details.photo) > 0:
            changes['photo_identifier'] = self.__save_photo(content=details.photo,
                                                            content_type=details.photo_content_type)
        self.__user_repository.update(
            identifier=identifier,
            changes=changes,
            added_roles=details.added_roles,
            removed_roles=details.removed_roles
        )

    def fetch_file(self, resp: falcon.Response, identifier: str) -> None:
        self.__file_storage.fetch(resp=resp, identifier=identifier)

    def __save_photo(self, content: bytes, content_type: str) -> str:
        identifier: str = "{}.{}".format(uuid.uuid4().hex, str(content_type).split("/")[1]).lower()
        self.__file_storage.save(
            identifier=identifier,
            content=content,
            content_type=content_type
        )
        return identifier
