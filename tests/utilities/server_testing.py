import unittest

from falcon.testing import TestClient
from app.app import Application
from app.configuration import Configuration
from app.core.database.migrations import SQLMigrationHandler
from app.settings import MIGRATIONS_FOLDER


class ServerTestCase(unittest.TestCase, TestClient):

    def setUp(self) -> None:
        super(ServerTestCase, self).setUp()
        self.application = Application(configuration=self.configuration())
        self.migration_handler = SQLMigrationHandler(
            database_url=self.configuration().database_uri(),
            migration_folder=MIGRATIONS_FOLDER
        )
        self.migration_handler.migrate()
        TestClient.__init__(self, self.application.run())

    def tearDown(self) -> None:
        self.migration_handler.rollback()

    @staticmethod
    def configuration():
        return Configuration.get_instance(testing=True)
