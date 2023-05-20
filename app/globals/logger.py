import logging
import os

from flask import Flask


class Sprinkles:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Logger:
    def __init__(self, app=None):
        self.logger = None
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.logger = logging.getLogger(app.name)
        self.logger.propagate = False
        ch = logging.StreamHandler()

        if os.environ.get("FLASK_DEBUG"):
            self.logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)

        if app.config.get("DEBUG"):
            self.logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            (
                f'{Sprinkles.OKGREEN}{app.name}{Sprinkles.END} '
                f'{Sprinkles.OKBLUE}IS{Sprinkles.END} '
                f'{Sprinkles.OKCYAN}%(message)s{Sprinkles.END}'
            )
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
