import json
import sys
import requests
from . import AbstractLogger


class Slack(AbstractLogger):

    def __init__(self, uri: str):
        self.uri = uri

    def write(self, message: str) -> None:
        payload = {
            'text': message,
        }

        try:
            requests.post(self.uri, json.dumps(payload))
        except:
            print("Unexpected error:", sys.exc_info()[0])

