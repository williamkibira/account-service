from app.domain.acm.roles.repository import RoleRepository


class RoleService(object):
    def __init__(self, repository: RoleRepository):
        self.__repository: RoleRepository = repository

    def save(self, name: str):
        self.__repository.save(name=name)

    def remove(self, name: str):
        self.__repository.remove(name=name)

    def search(self, query: str = '', limit: int = 10, offset: int = 0):
        roles = self.__repository.search(query=query, limit=limit, offset=offset)
        return [{'name': role.name, 'idx': role.index} for role in roles]
