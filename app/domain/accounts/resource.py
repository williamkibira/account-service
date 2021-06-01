import falcon
import simplejson as json
from app.core.security.authorization import Authorize
from app.domain.accounts.accounts_pb2 import RegistrationDetails, UpdateDetails
from app.domain.accounts.service import AccountService


class AccountCreationResource:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            details: RegistrationDetails = RegistrationDetails()
            details.ParseFromString(req.bounded_stream)
            identifier: str = self.__service.register(details=details)
            resp.status = falcon.HTTP_OK
            resp.body = json.dumps({'id': identifier})
        except IOError as err:
            resp.status = falcon.HTTP_417
            resp.body = json.dumps({'error': 417, 'message': str(err)})


@Authorize(roles=['PARTICIPANT'])
class AccountUpdateResource:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_put(self, req: falcon.Request, resp: falcon.Response) -> None:
        try:
            details: UpdateDetails = UpdateDetails()
            details.ParseFromString(req.bounded_stream)
            self.__service.update(details=details)
            resp.status = falcon.HTTP_NO_CONTENT

        except IOError as err:
            resp.status = falcon.HTTP_417
            resp.body = json.dumps({'error': 417, 'message': str(err)})


@Authorize(roles=['PARTICIPANT'])
class AccountImage:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_get(self, req: falcon.Request, resp: falcon.Response, identifier: str) -> None:
        self.__service.fetch_file(resp, identifier)


class ReceivePasswordResetRequest:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_put(self, req: falcon.Request, resp: falcon.Response) -> None:
        pass


class ResetAccountPassword:
    def __init__(self, service: AccountService):
        self.__service = service

    def on_put(self, req: falcon.Request, resp: falcon.Response) -> None:
        pass
