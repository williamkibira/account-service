import abc
from typing import List

from app.domain.acm.roles.models import Role


class RoleRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'save') and
                callable(subclass.save) and
                hasattr(subclass, 'remove') and
                callable(subclass.remove) and
                hasattr(subclass, 'search') and
                callable(subclass.search) and
                hasattr(subclass, 'fetch_all') and
                callable(subclass.fetch_all) or
                NotImplemented)

    @abc.abstractmethod
    def save(self, name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, query: str, limit: int, offset: int) -> List[Role]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_all(self) -> List[Role]:
        raise NotImplementedError
