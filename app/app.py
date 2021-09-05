import falcon
from decouple import config


from app.configuration import Configuration
from app.core.database.provider import SQLProvider
from app.core.health.health_checks import Readiness, Liveness, Ping
from app.core.security.argon2_password_handler import Argon2PasswordHandler
from app.core.security.password_handler import PasswordHandler
from app.core.server import CoreServerApplication
from app.core.storage.s3_storage import S3FileStorage
from app.core.storage.storage import FileStorage
from app.domain.accounts.emails.client import EmailClient
from app.domain.accounts.emails.http_client import HttpEmailClient
from app.domain.accounts.recovery.repository import RecoveryRepository
from app.domain.accounts.recovery.sql_repository import SQLRecoveryRepository
from app.domain.accounts.resource import AccountCreationResource, AccountUpdateResource, ProfilePicture, \
    ReceivePasswordResetRequest, ResetAccountPassword
from app.domain.accounts.service import AccountService
from app.domain.acm.roles.repository import RoleRepository
from app.domain.acm.roles.sql_repository import SQLRoleRepository
from app.domain.acm.users.repository import UserRepository
from app.domain.acm.users.sql_repository import SQLUserRepository


class ServerApplication(CoreServerApplication):

    def __init__(self, configuration: Configuration):
        self._configuration: Configuration = configuration
        self._file_storage: FileStorage = None
        self._email_client: EmailClient = None
        self._password_handler: PasswordHandler = None
        self._role_repository: RoleRepository = None
        self._user_repository: UserRepository = None
        self._recovery_repository: RecoveryRepository = None
        self._account_service: AccountService = None

    def initialize_resources(self) -> None:
        database_provider = SQLProvider(
            uri=self._configuration.database_uri(),
            debug=config('DEBUG', default=True, cast=bool))
        database_provider.initialize()
        if not self._configuration.is_in_test_mode():
            self._file_storage = S3FileStorage(credentials=self._configuration.s3_credentials())
            self._email_client = HttpEmailClient(self._configuration)
        self._role_repository = SQLRoleRepository(data_source=database_provider.provider())
        self._user_repository = SQLUserRepository(data_source=database_provider.provider())
        self._recovery_repository = SQLRecoveryRepository(data_source=database_provider.provider())
        self._password_handler = Argon2PasswordHandler(
            configuration=self._configuration.argon2_configuration()
        )

    def initialize_services(self) -> None:
        self._account_service = self._account_service = AccountService(
            file_storage=self._file_storage,
            user_repository=self._user_repository,
            password_handler=self._password_handler,
            recovery_repository=self._recovery_repository,
            email_client=self._email_client
        )

    def initialize_routes(self, app: falcon.App) -> None:
        app.add_route('/health-check', Readiness())
        app.add_route('/liveness', Liveness())
        app.add_route('/ping', Ping())
        app.add_route('/api/v1/account-service/accounts/register',
                      AccountCreationResource(service=self._account_service))
        app.add_route('/api/v1/account-service/accounts/update', AccountUpdateResource(service=self._account_service))
        app.add_route('/api/v1/account-service/accounts/profile-picture',
                      ProfilePicture(service=self._account_service))
        app.add_route('/api/v1/account-service/accounts/request-reset',
                      ReceivePasswordResetRequest(service=self._account_service))
        app.add_route('/api/v1/account-service/accounts/reset', ResetAccountPassword(service=self._account_service))

    def boot_prompt(self):
        build_information = self._configuration.build_information()
        self._info("Starting {} VER: {}".format(build_information.name(), build_information.version()))