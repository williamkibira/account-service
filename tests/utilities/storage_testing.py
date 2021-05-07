import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.database.base import BaseModel
from app.core.database.migrations import SQLMigrationHandler
from settings import DEBUG, DATABASE_URL, MIGRATIONS_FOLDER


class DatabaseResourceTests(unittest.TestCase):

    def setUp(self) -> None:
        self.migration_handler = SQLMigrationHandler(
            database_url=DATABASE_URL,
            migration_folder=MIGRATIONS_FOLDER
        )
        self.migration_handler.migrate()
        self.__debug = DEBUG
        engine = create_engine(
            DATABASE_URL,
            echo=DEBUG
        )
        session_factory = sessionmaker(bind=engine)
        self.session = scoped_session(session_factory)
        BaseModel.set_session(session=self.session)
        BaseModel.prepare(engine, reflect=True)

    def tearDown(self) -> None:
        self.migration_handler.rollback()



