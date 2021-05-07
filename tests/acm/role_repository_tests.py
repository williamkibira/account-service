import unittest
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.database.base import BaseModel
from app.core.database.connection import DataSource
from app.domain.acm.roles.models import Role
from app.domain.acm.roles.repository import RoleRepository
from app.domain.acm.roles.sql_repository import SQLRoleRepository
from app.settings import DATABASE_URL


class RoleRepositoryTests(unittest.TestCase):

    def setUp(self) -> None:
        engine = create_engine(
            DATABASE_URL,
            echo=True
        )

        session_factory = sessionmaker(bind=engine)
        session = scoped_session(session_factory)
        BaseModel.set_session(session=session)
        BaseModel.prepare(engine, reflect=True)
        self.repository: RoleRepository = SQLRoleRepository(data_source=DataSource(engine=engine))

    def test_can_add_role(self):
        self.repository.save(name="ADMINISTRATOR")
        roles: List[Role] = self.repository.fetch_all()
        self.assertEquals(1, )

    # test case function to check the Person.get_name function
    def test_1_get_name(self):
        pass


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
