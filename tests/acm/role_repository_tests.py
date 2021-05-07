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
        self.repository: RoleRepository = SQLRoleRepository(data_source=DataSource(session=session))

    def test_can_add_role(self):
        self.repository.save(name="ADMINISTRATOR")
        roles: List[Role] = self.repository.fetch_all()
        self.assertEquals(1, len(roles))
        self.assertEquals("ADMINISTRATOR", roles[0].name)
        self.assertEquals(1, roles[0].idx)

    # test case function to check the Person.get_name function
    def test_can_search_for_role(self):
        self.repository.save(name="ADMINISTRATOR")
        self.repository.save(name="AUDITOR")
        self.repository.save(name="AUTHOR")
        roles: List[Role] = self.repository.search(query="au", limit=2, offset=0)
        self.assertEquals(2, len(roles))
        names = [r.name for r in roles]
        self.assertListEqual(["AUDITOR", "AUTHOR"], names)

    def test_can_remove_role(self):
        self.repository.save(name="REBEL")
        roles: List[Role] = self.repository.fetch_all()
        self.assertTrue(len(roles) > 0)
        self.repository.remove(name="REBEL")
        roles: List[Role] = self.repository.fetch_all()
        self.assertEquals(0, len(roles))


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
