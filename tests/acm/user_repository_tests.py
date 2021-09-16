import unittest
import uuid
from typing import Optional, List

from app.core.database.connection import DataSource
from app.domain.acm.roles.repository import RoleRepository
from app.domain.acm.roles.sql_repository import SQLRoleRepository
from app.domain.acm.users.models import User
from app.domain.acm.users.repository import UserRepository
from app.domain.acm.users.sql_repository import SQLUserRepository
from tests.utilities.storage_testing import DatabaseResourceTests


class UserRepositoryTests(DatabaseResourceTests):
    def setUp(self) -> None:
        super(UserRepositoryTests, self).setUp()
        self.role_repository: RoleRepository = SQLRoleRepository(data_source=DataSource(session=self.session))
        self.user_repository: UserRepository = SQLUserRepository(data_source=DataSource(session=self.session))

    def tearDown(self) -> None:
        super(UserRepositoryTests, self).tearDown()

    def test_can_add_user(self):
        self.role_repository.save(name='ADMINISTRATOR')
        identifier = str(uuid.uuid4())
        user = User(
            identifier=identifier,
            first_name='Damian',
            last_name='Kasule',
            email_address='damian.kasule@gmail.com',
            nickname='kaldam',
            password='Fox**234590'
        )
        self.user_repository.save(user=user, roles=['ADMINISTRATOR'])
        result: Optional[User] = self.user_repository.fetch_by_identifier(identifier=identifier)
        self.assertEqual(identifier, result.identifier)
        self.assertEqual(user.first_name, result.first_name)
        self.assertEqual(user.last_name, result.last_name)
        self.assertEqual(user.email_address, result.email_address)
        self.assertEqual(user.nickname, result.nickname)
        self.assertEqual(user.password, result.password)
        self.assertIsNotNone(result.created_at)
        self.assertEqual('ADMINISTRATOR', result.roles[0].name)

    # test case function to check the Person.get_name function
    def test_can_update_user(self):
        self.role_repository.save(name='ADMINISTRATOR')
        self.role_repository.save(name='GROUP_MEMBER')
        identifier = str(uuid.uuid4())
        user = User(
            identifier=identifier,
            first_name='Gerald',
            last_name='Kamya',
            nickname='kamge',
            email_address='gerald.kamya@gmail.com',
            password='Gnx**KNO98'
        )
        self.user_repository.save(user=user, roles=['ADMINISTRATOR'])
        # UPDATE USER INFORMATION
        updated_information = {
            'first_name': 'Trevor',
            'last_name': 'Noah',
            'email_address': 'trevor.noah@gmail.com',
            'password': 'genos.gear'
        }
        added_roles = ['GROUP_MEMBER']
        removed_roles = ['ADMINISTRATOR']
        self.user_repository.update(
            identifier=identifier,
            changes=updated_information,
            added_roles=added_roles,
            removed_roles=removed_roles
        )
        result: Optional[User] = self.user_repository.fetch_by_identifier(identifier=identifier)
        self.assertEqual(updated_information['first_name'], result.first_name)
        self.assertEqual(updated_information['last_name'], result.last_name)
        self.assertEqual(updated_information['email_address'], result.email_address)
        self.assertEqual(updated_information['password'], result.password)
        self.assertListEqual(added_roles, [role.name for role in result.roles])
        self.assertTrue('ADMINISTRATOR' not in [role.name for role in result.roles])

    def test_can_search_for_user(self):
        self.role_repository.save(name='GROUP_MEMBER')
        identifier = str(uuid.uuid4())
        user = User(
            identifier=identifier,
            first_name='Peter',
            last_name='Kamara',
            email_address='peter.kamara@gmail.com',
            nickname='kampe',
            password='GnVB**KNO98'
        )
        self.user_repository.save(user=user, roles=['GROUP_MEMBER'])
        results: List[User] = self.user_repository.search(query='pet', limit=2, offset=0)
        self.assertEquals(1, len(results))
        self.assertEquals(user.first_name, results[0].first_name)
        self.assertEquals(user.last_name, results[0].last_name)
        self.assertEquals(user.email_address, results[0].email_address)
        self.assertEquals(user.password, results[0].password)

    def test_can_remove_user(self):
        self.role_repository.save(name='ADMINISTRATOR')
        identifier = str(uuid.uuid4())
        user = User(
            identifier=identifier,
            first_name='Damian',
            last_name='Kasule',
            nickname='damka',
            email_address='damian.kasule@gmail.com',
            password='Fox**234590'
        )
        self.user_repository.save(user=user, roles=['ADMINISTRATOR'])
        result: Optional[User] = self.user_repository.fetch_by_identifier(identifier=identifier)
        self.assertIsNotNone(result)
        self.user_repository.remove(identifier=identifier)
        result: Optional[User] = self.user_repository.fetch_by_identifier(identifier=identifier)
        self.assertIsNone(result)

    def test_can_fetch_batch_of_users(self):
        self.role_repository.save(name='ADMINISTRATOR')
        identifier = str(uuid.uuid4())
        user = User(
            identifier=identifier,
            first_name='Damian',
            last_name='Kasule',
            nickname='damka',
            email_address='damian.kasule@gmail.com',
            password='Fox**234590'
        )
        self.user_repository.save(user=user, roles=['ADMINISTRATOR'])
        results: List[User] = self.user_repository.fetch_batch(identifiers=[identifier])
        self.assertEquals(1, len(results))
        self.assertEquals(user.first_name, results[0].first_name)
        self.assertEquals(user.last_name, results[0].last_name)
        self.assertEquals(user.email_address, results[0].email_address)
        self.assertEquals(user.password, results[0].password)


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
