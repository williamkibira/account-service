import abc

from app.core.logging.loggers import LoggerMixin
from app.domain.accounts.emails.orders import PasswordReset, AccountDetails

REGISTRATION_LINK = "registration-confirmation"
PASSWORD_RESET_LINK = "password-reset"
TOPIC = "v1/email-service/single-email-order"
TIMEOUT_SECONDS = 10
REGISTRATION_SUBJECT = "COMZ Registration Confirmation"
PASSWORD_RECOVERY_SUBJECT = "COMZ CITES Password Recovery"
ACCOUNT_DETAILS_SUBJECT = "COMZ CITES Account Details"


class EmailClient(abc.ABC, LoggerMixin):
    @abc.abstractmethod
    def send_password_reset(self, order: PasswordReset = None) -> None:
        pass

    @abc.abstractmethod
    def send_credentials(self, order: AccountDetails = None) -> None:
        pass
