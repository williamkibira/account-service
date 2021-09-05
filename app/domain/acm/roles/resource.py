import falcon
import simplejson as json

from app.domain.acm.roles.service import RoleService


class RoleResource(object):
    def __init__(self, service: RoleService):
        self.__service = service

    def post(self, req: falcon.Request, resp: falcon.Response):
        payload = json.load(req.bounded_stream)
        self.__service.save(name=payload['name'])
        resp.status = falcon.HTTP_200

    def search(self, req: falcon.Request, resp: falcon.Response):
        roles = self.__service.search(query=req.params['q'], limit=req.params['limit'], offset=req.params['offset'])
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(roles)

    def remove(self, req: falcon.Request, resp: falcon.Response):
        payload = json.load(req.bounded_stream)
        self.__service.remove(name=payload['name'])
        resp.status = falcon.HTTP_204
