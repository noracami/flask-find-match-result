import os
from flask import Flask
from .config import DevelopmentConfig, ProductionConfig
from .database import mongo_client


app = Flask(__name__)

if app.config is None:
    if os.environ.get("FLASK_ENV") == "development":
        app.config.from_object(DevelopmentConfig)
    elif os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)


@app.route("/")
def index():
    return "Welcome, this is a Flask app deployed on Zeabur"


@app.route("/db-health-check")
def db_health_check():
    # print connection string
    print(mongo_client)
    # print database names
    try:
        return str(mongo_client.list_database_names())
    except Exception as e:
        return str(e)


@app.route("/visits")
def visits():
    # to increment the visits count
    mongo_client.aoe_find_match_result.visits.update_one(
        {"_id": "visits"}, {"$inc": {"count": 1}}, upsert=True
    )
    # to get the visits count
    count = mongo_client.aoe_find_match_result.visits.find_one({"_id": "visits"})
    return f"Total visits: {count['count']}"
