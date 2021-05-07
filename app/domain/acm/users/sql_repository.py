from typing import List, Dict

from app.core.database.connection import DataSource
from app.domain.acm.users.models import User
from app.domain.acm.users.repository import UserRepository


class SQLUserRepository(UserRepository):
    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def save(self, user: User):
        pass

    def update(self, identifier: str, changes: Dict):
        pass

    def remove(self, identifier: str):
        pass

    def fetch_batch(self, identifiers: Dict) -> List[User]:
        pass

    def search(self, query: str, limit: int, offset: int) -> List[User]:
        pass