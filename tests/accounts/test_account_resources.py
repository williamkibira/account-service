from typing import Dict

from falcon.testing.client import _ResultBase

from app.domain.accounts.accounts_pb2 import RegistrationDetails, UpdateDetails, PasswordResetRequest, PasswordReset
from tests.utilities.server_testing import ServerTestCase


class AuthorizationTestCase(ServerTestCase):

    def test_given_registration_information_account_will_be_created(self):
        result: _ResultBase = self.__register_user(details={
            'first_name': 'Vic',
            'last_name': 'Thorn',
            'email': 'vic.thorn@gmail.com',
            'role': 'PARTICIPANT',
            'password': 'viking'
        })
        print(result.json)
        self.assertEqual(200, result.status_code)
        self.assertIsInstance(result.json, dict)

    def test_given_an_existing_account_an_update_can_be_made(self):
        result: _ResultBase = self.__register_user(details={
            'first_name': 'Vic',
            'last_name': 'Thorn',
            'email': 'vic.thorn@gmail.com',
            'role': 'PARTICIPANT',
            'password': 'viking'
        })

        updates = UpdateDetails()
        updates.first_name = 'Vin'
        updates.last_name = 'Diesel'
        updates.email = "vin.diesel@gmail.com"
        updates.added_roles.append('ADMINISTRATOR')

        update_result = self.simulate_put(
            path='/api/v1/account-service/accounts/update',
            headers={'Authorization': self.authorization_for(identifier=result.json['id'], roles=['PARTICIPANT'])},
            content_type="application/x-protobuf",
            body=updates.SerializeToString()
        )
        self.assertEqual(204, update_result.status_code)

    def test_given_registered_account_an_invalid_update_will_fail(self):
        result: _ResultBase = self.__register_user(details={
            'first_name': 'Vic',
            'last_name': 'Thorn',
            'email': 'vic.thorn@gmail.com',
            'role': 'PARTICIPANT',
            'password': 'viking'
        })

        updates = UpdateDetails()
        updates.first_name = 'Vin'
        updates.last_name = 'Diesel'
        updates.added_roles.append('ADMINISTRATOR')

        update_result = self.simulate_put(
            path='/api/v1/account-service/accounts/update',
            headers={'Authorization': self.authorization_for(identifier=result.json['id'], roles=['PARTICIPANT'])},
            content_type="application/x-protobuf",
            body=updates.SerializeToString()
        )
        self.assertEqual(417, update_result.status_code)

    def test_given_a_registered_account_an_existing_accounts_password_can_be_reset(self):
        self.__register_user(details={
            'first_name': 'Vic',
            'last_name': 'Thorn',
            'email': 'vic.thorn@gmail.com',
            'role': 'PARTICIPANT',
            'password': 'viking'
        })
        reset_request = PasswordResetRequest()
        reset_request.email = "vic.thorn@gmail.com"
        request_result = self.simulate_post(
            path='/api/v1/account-service/accounts/request-reset',
            content_type="application/x-protobuf",
            body=reset_request.SerializeToString()
        )
        self.assertEqual(200, request_result.status_code)
        password_reset = PasswordReset()
        order = self._reset_orders[request_result.json['reference']]
        password_reset.reference = order.reference
        password_reset.otp = order.otp
        password_reset.password = "flamer#"

        request_result = self.simulate_put(
            path='/api/v1/account-service/accounts/reset',
            content_type="application/x-protobuf",
            body=password_reset.SerializeToString()
        )
        self.assertEqual(204, request_result.status_code)

    def __register_user(self, details: Dict) -> _ResultBase:
        registration_details: RegistrationDetails = RegistrationDetails()
        registration_details.first_name = details['first_name']
        registration_details.last_name = details['last_name']
        registration_details.email = details['email']
        registration_details.password = details['password']
        registration_details.photo = "FAKE-BINARY-DATA-FOR-PHOTO".encode()
        registration_details.photo_content_type = "image/png"
        registration_details.roles.append("PARTICIPANT")

        return self.simulate_post(
            path='/api/v1/account-service/accounts/register',
            content_type="application/x-protobuf",
            body=registration_details.SerializeToString()
        )
