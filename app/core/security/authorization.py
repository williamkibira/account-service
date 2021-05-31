from datetime import datetime
from typing import Dict

import falcon
import simplejson as json
from jwcrypto import jwk, jwe
from settings import PRIVATE_RSA_KEY, PRIVATE_RSA_KEY_PASSWORD, ACCEPTED_AUDIENCE


class Authorize(object):
    def __init__(self, roles):
        self._roles = roles

    def __call__(self, req: falcon.Request, resp: falcon.Response, resource, params):
        token = self.__strip_out_authorization_token(req=req)
        claims_payload = self.__extract_token_claims(encrypted_token=token)
        claims = json.loads(claims_payload)
        if self.__is_authorized_user(claims=claims):
            req.context["principals"] = claims
            req.context["access_token"] = token
        else:
            raise falcon.HTTPForbidden(title="No Authorization for this request",
                                       description="You do not have the required permissions to access this resource")

    def __is_authorized_user(self, claims: Dict) -> bool:
        token_roles = claims["roles"]
        for role in token_roles:
            if role in self._roles:
                return True
        return False

    def __extract_token_claims(self, encrypted_token: str) -> str:
        jwe_token = jwe.JWE()
        private_key = self.__read_private_key(path=PRIVATE_RSA_KEY)
        jwe_token.deserialize(encrypted_token, key=private_key)
        return jwe_token.payload

    @staticmethod
    def __strip_out_authorization_token(req: falcon.Request) -> str:
        if req.get_header('Authorization') is None:
            raise falcon.HTTPUnauthorized(title="No Authorization for this request",
                                          description="You haven't added `Authorization` to this request")
        return req.get_header('Authorization').split(" ")[1]

    @staticmethod
    def __read_private_key(path: str) -> jwk.JWK:
        with open(path, "rb") as private_key_file:
            key = jwk.JWK()
            if len(str(PRIVATE_RSA_KEY_PASSWORD)) > 0:
                key.import_from_pem(data=private_key_file.read(), password=PRIVATE_RSA_KEY_PASSWORD)
            else:
                key.import_from_pem(data=private_key_file.read())
            return key

    @staticmethod
    def __verify_claim(claim: Dict) -> None:
        expiry_date_time = datetime.fromtimestamp(int(claim['exp']))
        if ACCEPTED_AUDIENCE.trim() in claim['aud']:
            raise falcon.HTTPForbidden(title="This user is not permitted to access this service",
                                       description="You are not the intended audience for this service")
        if expiry_date_time < datetime.datetime.now():
            raise falcon.HTTPUnauthorized(title="Your session has expired",
                                          description="Your current session is past its duration. \n"
                                                      "Please login again to continue")
