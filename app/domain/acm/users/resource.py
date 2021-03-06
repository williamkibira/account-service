import falcon
import simplejson as json
from app.domain.acm.users.service import UserService


class UserSearchResource(object):
    def __init__(self, service: UserService):
        self.__service: UserService = service

    # THIS CALL WILL BE RESPONSIBLE FOR SEARCHING FOR OTHER USERS BY EMAIL
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        payload = json.load(req.bounded_stream)
        results = self.__service.fetch_batch(
            identifiers=payload['identifiers'],
            identifier_type=payload['identifier_type']
        )
        resp.body = json.dumps(results)
        resp.status = falcon.HTTP_OK


class UserFetchResource(object):
    def __init__(self, service: UserService):
        self.__service: UserService = service

    def on_get(self, req: falcon.Request, resp: falcon.Response, identifier: str) -> None:
        user = self.__service.fetch_by_identifier(identifier=identifier)
        resp.body = json.dumps(user)
        resp.status = falcon.HTTP_OK
