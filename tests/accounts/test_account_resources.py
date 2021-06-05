from app.domain.accounts.accounts_pb2 import RegistrationDetails
from tests.utilities.server_testing import ServerTestCase


class AuthorizationTestCase(ServerTestCase):

    def test_given_registration_information_account_will_be_created(self):
        registration_details: RegistrationDetails = RegistrationDetails()
        registration_details.first_name = "Vic"
        registration_details.last_name = "Thorn"
        registration_details.email = "vic.thorn@gmail.com"
        registration_details.password = "viking"
        # registration_details.photo = ""
        registration_details.photo_content_type = "image/png"
        registration_details.roles.append("PARTICIPANT")

        result = self.simulate_post(
            path='/api/v1/account-service/accounts/register',
            content_type="application/x-protobuf",
            body=registration_details.SerializeToString()
            )
        print(result.json)
        #self.assertEqual(result.json, self.claims)

