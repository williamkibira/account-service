from typing import List, Dict

from app.domain.acm.users.models import User
from app.domain.acm.users.repository import UserRepository


def package(user: User) -> Dict:
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'photo_identifier': user.photo_identifier,
        'identifier': user.identifier,
        'idx': user.index,
    }


class UserService:
    def __init__(self, repository: UserRepository):
        self.__repository: UserRepository = repository

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
