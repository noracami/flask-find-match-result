import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_HOST"),
        "port": os.environ.get("MONGODB_PORT"),
        "username": os.environ.get("MONGODB_USERNAME"),
        "password": os.environ.get("MONGODB_PASSWORD"),
    }
