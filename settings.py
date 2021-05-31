import os
from decouple import config

DEBUG = config('DEBUG', cast=bool, default=True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = config('DATABASE_URL', default='sqlite:///sample.db')
MIGRATIONS_FOLDER = os.path.join(BASE_DIR, "resources/migrations")
STORAGE_HOST = config('STORAGE_BUCKET', default='')
STORAGE_BUCKET = config('STORAGE_BUCKET', default='')
STORAGE_KEY = config('STORAGE_KEY', default='')
STORAGE_SECRET = config('STORAGE_SECRET', default='')
STORAGE_REGION = config('STORAGE_REGION', default='')

# SECURITY AUTHORIZATION PARAMETERS
PRIVATE_RSA_KEY = os.path.join(BASE_DIR, "/resources/keys/private-rsa-key.pem")
PRIVATE_RSA_KEY_PASSWORD = config('RSA_KEY_PASSWORD', default='')
ACCEPTED_AUDIENCE = config('ACCEPTED_AUDIENCE', default='')
