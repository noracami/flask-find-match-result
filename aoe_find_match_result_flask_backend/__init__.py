import os
from flask import Flask, request
from flask_cors import CORS
from .config import DevelopmentConfig, ProductionConfig
from .database import mongo_client


app = Flask(__name__)
CORS(app)

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


# POST /matches => create a new match
# GET /matches => get all matches
@app.route("/api/v1/matches", methods=["POST", "GET"])
def matches():
    if request.method == "POST":
        return create_match()
    elif request.method == "GET":
        return get_all_matches()


def create_match():
    match = request.json
    mongo_client.aoe_find_match_result.matches.insert_one(
        {"_id": match["matchId"], **match}
    )
    return "Match created successfully", 201


def get_all_matches():
    # 1. get all matches
    # 2. group by match_id
    # 3. take the latest match (the one with the highest timestamp)
    matches = mongo_client.aoe_find_match_result.matches.aggregate(
        [{"$group": {"_id": "$matchId", "latest_match": {"$max": "$timestamp"}}}]
    )
    return matches, 200


# GET /matches/<id> => get a single match
@app.route("/api/v1/matches/<id>")
def get_match(id):
    # 1. get matches by match_id
    # 2. sort by timestamp
    # 3. get the latest match (the one with the highest timestamp)
    match = (
        mongo_client.aoe_find_match_result.matches.find({"matchId": id})
        .sort("timestamp", -1)
        .limit(1)
    )
    return match, 200
