import abc
from typing import Dict, List, Optional

from app.domain.acm.users.models import User


class UserRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'save') and
                callable(subclass.save) and
                hasattr(subclass, 'update') and
                callable(subclass.update) and
                hasattr(subclass, 'remove') and
                callable(subclass.remove) and
                hasattr(subclass, 'fetch_batch') and
                callable(subclass.fetch_batch) and
                hasattr(subclass, 'search') and
                callable(subclass.search) or
                NotImplemented)

    @abc.abstractmethod
    def save(self, user: User, roles: List[str]):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, identifier: str, changes: Dict, added_roles: List[str], removed_roles: List[str]):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_by_identifier(self, identifier: str) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, identifier: str):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_batch(self, identifiers: Dict) -> List[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, query: str, limit: int, offset: int) -> List[User]:
        raise NotImplementedError
