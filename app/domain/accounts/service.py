import math
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, Optional
import falcon

from app.core.logging.loggers import Logger, LoggerMixin
from app.core.security.password_handler import PasswordHandler
from app.core.storage.storage import FileStorage
from app.domain.accounts.accounts_pb2 import RegistrationDetails, UpdateDetails, PasswordResetRequest
from app.domain.accounts.emails.client import EmailClient
from app.domain.accounts.emails.orders import PasswordReset
from app.domain.accounts.recovery.repository import RecoveryRepository
from app.domain.acm.users.models import User
from app.domain.acm.users.repository import UserRepository

ALPHA_NUMERIC = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class AccountService(LoggerMixin):
    def __init__(self,
                 file_storage: FileStorage,
                 user_repository: UserRepository,
                 password_handler: PasswordHandler,
                 recovery_repository: RecoveryRepository,
                 email_client: EmailClient):
        self.__file_storage: FileStorage = file_storage
        self.__user_repository: UserRepository = user_repository
        self.__recovery_repository: RecoveryRepository = recovery_repository
        self.__password_handler: PasswordHandler = password_handler
        self.__email_client: EmailClient = email_client
        self.log = Logger(__file__)

    def register(self, details: RegistrationDetails) -> str:
        identifier = str(uuid.uuid4())
        self.log.info("IDENTIFY: {}".format(identifier))
        self.log.info("FIRST NAME: {}".format(details.first_name))
        self.log.info("LAST NAME: {}".format(details.last_name))
        self.log.info("EMAIL: {}".format(details.email))
        self.log.info("PASSWORD: {}".format(details.password))
        hashed_password: str = self.__password_handler.hash(password=details.password)
        self.log.info("ENCODED PASSWORD: {}".format(hashed_password))
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
        for (key, value) in changes.items():
            if len(value) == 0:
                raise falcon.HTTPError(status="417",
                                       title="Invalid entry for field {0}".format(key),
                                       description="Please give a valid entry for {0}".format(key),
                                       code=falcon.HTTP_417)
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

    def route_password_reset_request(self, password_reset_request: PasswordResetRequest) -> str:
        reference: str = str(uuid.uuid4())
        otp: str = self.generate_otp()
        due_date = datetime.utcnow() + timedelta(minutes=5)
        if self.__recovery_repository.add_request(reference=reference,
                                                  otp=otp,
                                                  due_date=due_date,
                                                  email_address=password_reset_request.email):
            order = PasswordReset(reference=reference, email=password_reset_request.email, otp=otp)
            self.__email_client.send_password_reset(order=order)
            return reference

    def reset_password(self, order: PasswordReset) -> None:
        identifier: Optional[str] = self.__recovery_repository.fetch_user_identifier(reference=order.reference)
        if identifier is not None and len(order.password) > 0:
            hashed_password: str = self.__password_handler.hash(password=order.password)
            self.log.info("ENCODED PASSWORD: {}".format(hashed_password))
            self.__user_repository.update(
                identifier=identifier,
                changes={'password': hashed_password},
                added_roles=[],
                removed_roles=[]
            )
        else:
            self._info("No valid changes to effect, try sending another recovery request instead")
            raise falcon.HTTPError(status="404",
                                   title="No match found for recovery order with OTP: {}".format(order.otp),
                                   description="Your OTP is either invalid or has expired")

    @staticmethod
    def generate_otp():
        otp = ""
        length = len(ALPHA_NUMERIC)
        for i in range(6):
            otp += ALPHA_NUMERIC[math.floor(random.random() * length)]
        return otp
