import logging
import sys
import threading
from os import path
from typing import Dict

import boto3
import falcon
from botocore.client import BaseClient
from botocore.config import Config
from botocore.exceptions import ClientError

from app.core.storage.storage import FileStorage
from settings import STORAGE_SECRET, STORAGE_REGION, STORAGE_KEY, STORAGE_HOST, STORAGE_BUCKET


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


class S3FileStorage(FileStorage):

    def __init__(self):
        self.__client: BaseClient = boto3.client(
            's3',
            endpoint_url=STORAGE_HOST,
            region_name=STORAGE_REGION,
            aws_access_key_id=STORAGE_KEY,
            aws_secret_access_key=STORAGE_SECRET,
            config=Config(signature_version='s3v4'),
        )

    def save(self, identifier: str, content: bytes, content_type: str):
        try:
            response: Dict = self.__client.put_object(
                Bucket=STORAGE_BUCKET,
                Body=content,
                Key=identifier,
                Callback=ProgressPercentage(filename=identifier),
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": content_type
                }
            )
            logging.info("{}".format(response))
        except ClientError as e:
            logging.error(e)

    def fetch(self, response: falcon.Response, identifier: str):
        data_object: Dict = self.__client.get_object(
            Bucket=STORAGE_BUCKET,
            Key=identifier
        )
        response.data = data_object['Body'].read()
        response.downloadable_as = identifier
        response.content_type = data_object['ContentType']
        response.content_length = data_object['ContentLength']
        response.content_range = data_object['ContentRange']
        response.set_header(name='ContentDisposition', value=data_object['ContentDisposition'])

    def remove(self, identifier: str):
        response: Dict = self.__client.delete_object(
            Bucket=STORAGE_BUCKET,
            Key=identifier
        )
