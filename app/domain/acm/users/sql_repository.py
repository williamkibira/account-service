from typing import List, Dict, Optional

from app.core.database.connection import DataSource
from app.domain.acm.users.models import User
from app.domain.acm.users.repository import UserRepository


class SQLUserRepository(UserRepository):
    def fetch_by_identifier(self, identifier: str) -> Optional[User]:
        pass

    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def save(self, user: User, roles: List[str]):
        pass

    def update(self, identifier: str, changes: Dict, added_roles: List[str], removed_roles: List[str]):
        pass

    def remove(self, identifier: str):
        pass

    def fetch_batch(self, identifiers: Dict) -> List[User]:
        pass

    def search(self, query: str, limit: int, offset: int) -> List[User]:
        pass
