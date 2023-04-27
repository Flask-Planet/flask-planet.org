from flask_bigapp import BigApp
from flask_sqlalchemy import SQLAlchemy

from app.globals.logger import Logger

bigapp = BigApp()
db = SQLAlchemy()
logger = Logger()
