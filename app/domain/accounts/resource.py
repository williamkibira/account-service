import falcon
import simplejson as json

from app.core.security.authorization import Restrict
from app.domain.accounts.accounts_pb2 import RegistrationDetails, UpdateDetails, PasswordResetRequest, PasswordReset
from app.domain.accounts.service import AccountService


class AccountCreationResource:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            details: RegistrationDetails = RegistrationDetails()
            details.ParseFromString(req.bounded_stream.read())
            identifier: str = self.__service.register(details=details)
            resp.status = falcon.HTTP_CREATED
            resp.body = json.dumps({'id': identifier})
        except IOError as err:
            resp.status = falcon.HTTP_417
            resp.body = json.dumps({'error': 417, 'message': str(err)})


@falcon.before(Restrict(roles=['PARTICIPANT']))
class AccountUpdateResource:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_put(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            details: UpdateDetails = UpdateDetails()
            details.ParseFromString(req.bounded_stream.read())
            self.__service.update(identifier=req.context['principals'].subject(), details=details)
            resp.status = falcon.HTTP_NO_CONTENT

        except IOError as err:
            resp.status = falcon.HTTP_417
            resp.body = json.dumps({'error': 417, 'message': str(err)})


class ReceivePasswordResetRequest:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            reset_request: PasswordResetRequest = PasswordResetRequest()
            reset_request.ParseFromString(req.bounded_stream.read())
            reference: str = self.__service.route_password_reset_request(password_reset_request=reset_request)
            resp.status = falcon.HTTP_OK
            resp.body = json.dumps({'reference': reference})
        except IOError as err:
            resp.status = falcon.HTTP_417
            resp.body = json.dumps({'error': 417, 'message': str(err)})


class ResetAccountPassword:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_put(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            password_request: PasswordReset = PasswordReset()
            password_request.ParseFromString(req.bounded_stream.read())
            self.__service.reset_password(order=password_request)
            resp.status = falcon.HTTP_NO_CONTENT
        except IOError as err:
            resp.status = falcon.HTTP_417
            resp.body = json.dumps({'error': 417, 'message': str(err)})
