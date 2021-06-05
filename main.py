import falcon

from app.app import Application
from app.configuration import Configuration


def run() -> falcon.API:
    application = Application(configuration=Configuration.get_instance())
    return application.run()
