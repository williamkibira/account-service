from os import path

BASE_DIRECTORY = path.dirname(path.abspath(__file__))

RESOURCES_DIRECTORY = path.join(BASE_DIRECTORY, "../resources")

MIGRATIONS_FOLDER = path.join(RESOURCES_DIRECTORY, "migrations")
PRIVATE_RSA_KEY = path.join(RESOURCES_DIRECTORY, "keys/private-rsa-key.pem")
PUBLIC_RSA_KEY = path.join(RESOURCES_DIRECTORY, "keys/public-rsa-key.pem")
EXISTING_ROLES = path.join(RESOURCES_DIRECTORY, "defaults/roles.json")
