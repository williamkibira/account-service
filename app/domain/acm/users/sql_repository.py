from typing import List, Dict, Optional

from sqlalchemy import and_, or_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.core.database.connection import DataSource
from app.domain.acm.roles.models import Role
from app.domain.acm.users.models import User, association_table
from app.domain.acm.users.repository import UserRepository


class SQLUserRepository(UserRepository):

    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def save(self, user: User, roles: List[str]):
        with self.__data_source.session as session:
            role_entities = session.query(Role).filter(Role.name.in_(roles)).all()
            for role in role_entities:
                user.roles.append(role)
            session.add(user)

    def fetch_by_identifier(self, identifier: str) -> Optional[User]:
        try:
            session = self.__data_source.unbound()
            return session.query(User).options(joinedload(User.roles)).filter(User.identifier == identifier).one()
        except NoResultFound as error:
            print("ERROR: {}".format(error))
            return None

    def update(self, identifier: str, changes: Dict, added_roles: List[str], removed_roles: List[str]):
        with self.__data_source.session as session:
            user = session.query(User) \
                .options(joinedload(User.roles)) \
                .filter(User.identifier == identifier) \
                .one()

            if len(removed_roles) != 0:
                roles_to_remove = [r.id for r in session.query(Role.id).filter(Role.name.in_(removed_roles)).all()]
                session \
                    .query(association_table) \
                    .filter(and_(
                    association_table.c.user_id == user.id,
                    association_table.c.role_id.in_(roles_to_remove))
                ).delete()

            if len(added_roles) != 0:
                roles_to_add = session.query(Role).filter(Role.name.in_(added_roles)).all()
                for role in roles_to_add:
                    user.roles.append(role)
            user.update(**changes)
            session.add(user)

    def remove(self, identifier: str):
        with self.__data_source.session as session:
            session.query(User).filter(User.identifier == identifier).delete()

    def fetch_batch(self, identifiers: List[str]) -> List[User]:
        session = self.__data_source.unbound()
        return [user for user in session.query(User).filter(User.identifier.in_(identifiers)).all()]

    def fetch_by_emails(self, emails: List[str]) -> List[User]:
        session = self.__data_source.unbound()
        return [user for user in session.query(User).filter(User.email_address.in_(emails)).all()]

    def search(self, query: str, limit: int, offset: int) -> List[User]:
        if len(query) == 0:
            return self.__search_without_query(limit=limit, offset=offset)
        return self.__search_with_query(query=query, limit=limit, offset=offset)

    def __search_without_query(self, limit: int, offset: int) -> List[User]:
        session = self.__data_source.unbound()
        return [user for user in session.query(User).filter(User.index > offset).limit(limit).all()]

    def __search_with_query(self, query: str, limit: int, offset: int) -> List[User]:
        session = self.__data_source.unbound()
        q = "%{}%".format(query.lower())
        results = session.query(User).filter(and_(
            User.index > offset,
            or_(
                User.first_name.ilike(q),
                User.last_name.ilike(q),
                User.email_address.ilike(q)
            ))).limit(limit).all()
        return [user for user in results]
