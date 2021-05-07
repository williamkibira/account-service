from typing import List

from app.core.database.connection import DataSource
from app.domain.acm.roles.models import Role
from app.domain.acm.roles.repository import RoleRepository


class SQLRoleRepository(RoleRepository):

    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def save(self, name: str):
        sql: str = "INSERT INTO role_tb(name) VALUES(:name)"
        with self.__data_source.session as session:
            session.execute(statement=sql, params={'name': name})

    def remove(self, name: str):
        sql: str = "DELETE FROM role_tb WHERE name = :name"
        with self.__data_source.session as session:
            session.execute(statement=sql, params={'name': name})

    def search(self, query: str, limit: int, offset: int) -> List[Role]:
        results: List[Role] = []
        sql: str = "SELECT name, idx FROM role_tb WHERE  idx > :offset"
        parameters = {}
        if len(query) > 0:
            q: str = "%" + query.lower() + "%"
            sql: str = "{} AND LOWER(name) LIKE :q ORDER BY name LIMIT :limit".format(sql)
            parameters = {'offset': offset, 'q': q, 'limit': limit}
        else:
            sql: str = "{} ORDER BY name LIMIT :limit".format(sql)
            parameters = {'offset': offset, 'limit': limit}
        with self.__data_source.session as session:
            rows = session.execute(statement=sql, params=parameters)
            results = [Role(name=r.name, index=r.idx) for r in rows]
        return results

    def fetch_all(self) -> List[Role]:
        results: List[Role] = []
        sql: str = "SELECT name, idx FROM role_tb"
        with self.__data_source.session as session:
            rows = session.execute(statement=sql)
            results = [Role(name=r.name, index=r.idx) for r in rows]
        return results
