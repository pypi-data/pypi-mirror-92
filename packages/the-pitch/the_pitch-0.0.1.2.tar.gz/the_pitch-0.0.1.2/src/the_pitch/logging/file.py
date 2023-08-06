import logging
from . import AbstractLogger


class LogFile(AbstractLogger):

    def __init__(self, filename: str):
        logging.basicConfig(filename, level=logging.DEBUG)

    def write(self, message: str) -> None:
        logging.info(message)
