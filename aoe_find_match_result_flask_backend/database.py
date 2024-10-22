import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .config import Config, DevelopmentConfig, ProductionConfig


class MongoDB:
    def __init__(self, config: Config):
        if config:
            self.config = config
            self.client = MongoClient(
                host=self.config.MONGODB_SETTINGS["host"],
                port=self.config.MONGODB_SETTINGS["port"],
                username=self.config.MONGODB_SETTINGS.get("username"),
                password=self.config.MONGODB_SETTINGS.get("password"),
                server_api=ServerApi("1"),
            )
        else:
            self.client = None

    def get_client(self):
        return self.client


if os.environ.get("FLASK_ENV") == "development":
    config = DevelopmentConfig
elif os.environ.get("FLASK_ENV") == "production":
    config = ProductionConfig
else:
    config = None

mongo_client = MongoDB(config).get_client()
