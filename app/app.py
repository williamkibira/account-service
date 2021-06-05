import falcon
from decouple import config

from app.core.database.provider import SQLProvider
from app.core.health.health_checks import Readiness, Liveness, Ping
from app.core.logging.loggers import Logger
from app.core.middleware.prometheus import PrometheusMiddleware
from app.core.security.argon2_password_handler import Argon2PasswordHandler
from app.core.security.password_handler import PasswordHandler
from app.core.storage.s3_storage import S3FileStorage
from app.core.storage.storage import FileStorage
from app.domain.accounts.resource import AccountCreationResource, AccountUpdateResource, ProfilePicture, \
    ReceivePasswordResetRequest, ResetAccountPassword
from app.domain.accounts.service import AccountService
from app.domain.acm.users.repository import UserRepository
from app.domain.acm.users.sql_repository import SQLUserRepository
from app.configuration import Configuration
from prometheus_client import CollectorRegistry


class Application:
    def __init__(self, configuration: Configuration):
        self.__configuration: Configuration = configuration
        self.__collector_registry: CollectorRegistry = CollectorRegistry()

    def __initialize(self, name: str, version: str) -> falcon.App:
        database_provider = SQLProvider(
            uri=self.__configuration.database_uri(),
            debug=config('DEBUG', default=True, cast=bool))
        database_provider.initialize()
        file_storage: FileStorage = S3FileStorage(credentials=self.__configuration.s3_credentials())

        app: falcon.App = falcon.App(
            cors_enable=True,
            middleware=[
                PrometheusMiddleware(register=self.__collector_registry),
            ])

        user_repository: UserRepository = SQLUserRepository(data_source=database_provider.provider())
        password_handler: PasswordHandler = Argon2PasswordHandler(
            configuration=self.__configuration.argon2_configuration()
        )
        account_service = AccountService(file_storage=file_storage,
                                         user_repository=user_repository,
                                         password_handler=password_handler)
        app.add_route('/health-check', Readiness())
        app.add_route('/liveness', Liveness())
        app.add_route('/ping', Ping())
        app.add_route('/api/v1/account-service/accounts/register', AccountCreationResource(service=account_service))
        app.add_route('/api/v1/account-service/accounts/update', AccountUpdateResource(service=account_service))
        app.add_route('/api/v1/account-service/accounts/profile-picture', ProfilePicture(service=account_service))
        app.add_route('/api/v1/account-service/accounts/request-reset',
                      ReceivePasswordResetRequest(service=account_service))
        app.add_route('/api/v1/account-service/accounts/reset', ResetAccountPassword(service=account_service))
        # Addition of first domain apis
        Logger(__file__).info("{} VERSION:{}".format(name, version))
        return app

    def run(self) -> falcon.App:
        build_information = self.__configuration.build_information()
        Logger(build_information.name()).info("Starting {}".format(build_information.name()))
        return self.__initialize(name=build_information.name(), version=build_information.version())
