from typing import List

from app.core.database.connection import DataSource
from app.domain.acm.roles.models import Role
from app.domain.acm.roles.repository import RoleRepository


class SQLRoleRepository(RoleRepository):

    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def save(self, name: str):
        with self.__data_source.session as session:
            session.add(Role(name=name))

    def remove(self, identifier: str):
        with self.__data_source.session as session:
        pass

    def search(self, query: str, limit: int, offset: int) -> List[Role]:
        pass

    def fetch_all(self) -> List[Role]:
        pass
