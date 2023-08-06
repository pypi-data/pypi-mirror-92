import os
import json


class Cache(object):
    def __init__(self, seed_contents: str = '{}') -> None:
        self.contents = seed_contents

    def write(self, data: dict) -> None:
        self.contents = json.dumps(data)

    def read(self) -> dict:
        return json.loads(self.contents)

class LocalCache(object):
    def __init__(self, path: str) -> None:
        self.path = path

    def write(self, data) -> None:
        with open(self.path, 'w') as output:
            output.write(
              json.dumps(data)
            )

    def read(self):
        if not os.path.exists(self.path):
            return {}

        contents = ''
        with open(self.path, 'r') as input:
            contents = input.read()

        return json.loads(contents)
