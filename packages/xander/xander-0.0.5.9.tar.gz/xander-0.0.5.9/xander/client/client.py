import json
import socket
from uuid import uuid4

import requests

from xander.client.routes import *
from xander.utils.client_utils import update
from xander.utils.constants import *


def create_url(*args):
    """
    Receive a list of strings and create the url.

    @param args: list of strings
    @return: url
    """

    url = '/'.join(args)
    return url


class XanderClient:

    def __init__(self, api_auth_file, logger, server_address='35.192.211.33', server_port=5000, local_mode=False):

        self.server_address = server_address if not local_mode else '127.0.0.1'
        self.server_port = server_port
        self.logger = logger
        self.api = None
        self.api_auth_file = api_auth_file
        self.run_id = uuid4().hex
        self.is_auth = False
        self.hostname = socket.gethostname()

    def connect(self):
        try:
            self.api = json.load(open(self.api_auth_file, 'r'))

            success, payload = self.make_post_request(url='api/test_api_token', asynchronous=False)

            if success:
                self.logger.info('You are logged as {} ({})'.format(self.api['user_name'], self.api['user_mail']))
                self.logger.info('Cloud mode is active.')
                self.is_auth = True
            else:
                raise Exception

        except FileNotFoundError as e:
            self.logger.info('Local mode is active, API auth file not found!')

        except Exception as e:
            self.logger.info('Local mode is active, connection to server failed!')

    def make_post_request(self, url, payload=None, asynchronous=True):
        payload = {} if payload is None else payload

        # Add project slug and run id
        payload[PROJECT_SLUG] = self.api['project_id']
        payload[RUN_ID] = self.run_id
        payload[USER_MAIL] = self.api['user_mail']

        headers = {}
        if self.api['api_token']:
            headers = {'Authorization': 'api_token {}'.format(self.api['api_token'])}

        url = 'http://{}:{}/{}'.format(self.server_address, self.server_port, url)

        return update(url=url, payload=payload, headers=headers, asynchronous=asynchronous, logger=self.logger)

    def save_run(self, execution):

        self.run_id = execution[RUN_ID]

        execution[HOSTNAME] = self.hostname

        return self.make_post_request(url=create_url(API, PUSH_RUN), payload=execution)

    def save_pipeline(self, pipeline):
        """
        Call the server and add the pipeline.

        @param pipeline:
        @return:
        """

        if not self.is_auth:
            return None

        payload = {
            PIPELINE_NAME: pipeline.pipeline_name,
            PIPELINE_SLUG: pipeline.pipeline_slug,
            START_TIME: pipeline.start_time,
            END_TIME: pipeline.end_time,
            DURATION: pipeline.run_duration
        }

        return self.make_post_request(url=create_url(API, PUSH_PIPELINE), payload=payload)
