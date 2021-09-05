from app.configuration import Configuration
from app.domain.accounts.emails.client import EmailClient
from app.domain.accounts.emails.orders import AccountDetails, PasswordReset


class HttpEmailClient(EmailClient):
    def __init__(self, configuration: Configuration):
        self.__configuration = configuration

    def send_password_reset(self, order: PasswordReset = None) -> None:
        pass

    def send_credentials(self, order: AccountDetails = None) -> None:
        pass
