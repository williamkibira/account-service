from typing import Dict

import falcon

from app.core.logging.loggers import Logger
from app.core.storage.storage import FileStorage


class FakeFileStorage(FileStorage):
    def __init__(self):
        self.log: Logger = Logger(__file__)
        self.__contents: Dict = {}

    def save(self, identifier: str, content: bytes, content_type: str):
        self.__contents[identifier] = content
        self.log.info("ADDED FOR: {}".format(identifier))

    def fetch(self, response: falcon.Response, identifier: str) -> None:
        response.data = self.__contents[identifier]
        response.content_type = "image/png"
        response.status = falcon.HTTP_OK

    def remove(self, identifier: str):
        del self.__contents[identifier]
