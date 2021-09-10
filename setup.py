from typing import List

from decouple import config
import simplejson as json
from app.configuration import Configuration
from app.core.database.provider import SQLProvider
from app.domain.acm.roles.sql_repository import SQLRoleRepository
from app.settings import EXISTING_ROLES


def main():
    configuration = Configuration.get_instance()
    database_provider = SQLProvider(
        uri=configuration.database_uri(),
        debug=config('DEBUG', default=True, cast=bool))
    database_provider.initialize()
    repository = SQLRoleRepository(data_source=database_provider.provider())
    roles: List[str] = read_roles()
    for role in roles:
        repository.save(name=role)


def read_roles() -> List[str]:
    roles = []
    with open(EXISTING_ROLES, "rb") as role_reader:
        roles = json.load(role_reader)
    return roles


if __name__ == "__main__":
    main()
