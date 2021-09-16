from typing import List, Dict

from app.configuration import Configuration
from app.domain.acm.users.models import User
from app.domain.acm.users.repository import UserRepository


def package(user: User, base_bucket_url: str) -> Dict:
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'nickname': user.nickname,
        'email_address': user.email_address,
        'photo_url': "{0}/{1}".format(base_bucket_url, user.photo_identifier),
        'identifier': user.identifier,
        'idx': user.index,
    }


class UserService:
    def __init__(self, repository: UserRepository, configuration: Configuration):
        self.__repository: UserRepository = repository
        self.__configuration: Configuration = configuration

    def fetch_batch(self, identifiers: List[str], identifier_type: str) -> List[Dict]:
        if identifier_type == 'EMAILS':
            return self.__search_by_email(emails=identifiers)
        elif identifier_type == 'IDENTIFIERS':
            return self.__fetch_identifier_batch(identifiers=identifiers)

    def __search_by_email(self, emails: List[str]) -> List[Dict]:
        users = self.__repository.fetch_by_emails(emails=emails)
        return [package(user) for user in users]

    def __fetch_identifier_batch(self, identifiers: List[str]) -> List[Dict]:
        users = self.__repository.fetch_batch(identifiers=identifiers)
        return [package(user) for user in users]

    def fetch_by_identifier(self, identifier) -> Dict[str]:
        user = self.__repository.fetch_by_identifier(identifier=identifier)
        return package(user=user, base_bucket_url="{0}/{1}".format(
            self.__configuration.s3_credentials().url(),
            self.__configuration.s3_credentials().bucket()
        ))
