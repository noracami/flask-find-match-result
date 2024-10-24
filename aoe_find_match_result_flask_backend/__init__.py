import os
from flask import Flask, request
from flask_cors import CORS
from .config import DevelopmentConfig, ProductionConfig
from .database import mongo_client
from bson.objectid import ObjectId

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
    # query for the matchId and finished fields, if it exists, do not insert, return 200
    if mongo_client.aoe_find_match_result.matches.find_one(
        {"matchId": match["matchId"], "finished": match["finished"]}
    ):
        return {"message": "Match already exists"}, 200

    mongo_client.aoe_find_match_result.matches.insert_one(match)
    # create index on matchId if not exists
    mongo_client.aoe_find_match_result.matches.create_index("matchId", unique=False)
    return {"message": "Match created successfully"}, 201


def get_all_matches():
    matches = list(mongo_client.aoe_find_match_result.matches.find())
    for match in matches:
        match["_id"] = str(match["_id"])

    return {"matches": matches}, 200

    # # 1. get all matches
    # # 2. group by match_id
    # # 3. take the latest match (the one with the highest timestamp)
    # matches = mongo_client.aoe_find_match_result.matches.aggregate(
    #     [{"$group": {"_id": "$matchId", "latest_match": {"$max": "$timestamp"}}}]
    # )
    # # delete the _id field since it's not JSON serializable
    # for match in matches:
    #     match.pop("_id")
    # return {"matches": list(matches)}, 200


# GET /matches/<id> => get a single match
@app.route("/api/v1/matches/<id>")
def get_match(id):
    # 1. get matches by match_id
    # 2. sort by timestamp
    # 3. get the latest match (the one with the highest timestamp)
    if not id.isdigit():
        return {"message": "Match ID must be an integer"}, 400

    match = mongo_client.aoe_find_match_result.matches.find({"matchId": int(id)}).sort(
        "timestamp", -1
    )[0]

    # delete the _id field since it's not JSON serializable
    match.pop("_id")
    return {"match": match}, 200
