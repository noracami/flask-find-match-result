import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGO_HOST"),
        "port": int(os.environ.get("MONGO_PORT")),
        "username": os.environ.get("MONGO_USERNAME"),
        "password": os.environ.get("MONGO_PASSWORD"),
    }
