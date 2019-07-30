import pymongo
import json
import requests
import os
from flask import Flask, jsonify, request
from flask_cors import CORS


# .ENV
from dotenv import load_dotenv
load_dotenv()

TOKEN1 = os.getenv('TOKEN1')
MONGO_USER1 = os.getenv('MONGO_USER1')
MONGO_PW1 = os.getenv('MONGO_PW1')

app = Flask(__name__)
# Added cors
cors = CORS(app, resources={r"/*": {"origins": "*"}})


myclient = pymongo.MongoClient(
    f"mongodb+srv://{MONGO_USER1}:{MONGO_PW1}@treasureseeker-b4iam.mongodb.net/test?retryWrites=true&w=majority")

mydb = myclient["treasuretracker"]
mycol = mydb["map"]

mydict = {"room": "Hall"}

# x = mycol.insert_one(mydict)direction

for x in mycol.find():
    print(x)

dblist = myclient.list_database_names()
if "treasuretracker" in dblist:
    print("The database exists.")

collist = mydb.list_collection_names()
if "map" in collist:
    print("The collection exists.")

map = [
    {
        0: {
            "room_id": 0,
            "title": "Room 0",
            "description": "You are standing in an empty room.",
            "coordinates": "(60,60)",
            "players": [],
            "items": ["small treasure"],
            "exits": ["n", "s", "e", "w"],
            "cooldown": 60.0,
            "errors": [],
            "messages": []
        }
    }
]

# Map ---------------------------------------------------
@app.route("/", methods=['GET'])
def index():
    return "API Running"


@app.route('/map', methods=['GET'])
def get_map():
    return jsonify(map)

# @app.route('/move')
@app.route('/move', methods=["POST"])
def move_player():
    # send request to lambda server with direction
    direction = request.get_json()['direction']
    print("DIRECTION: ", direction)
    if direction in ['n','e','w','s']:
        API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
        headers = {
            "Authorization": f'token {TOKEN1}'
        }
        data = {'direction': direction}
        print('DATAAAAAAAAA: ', data)
        r = requests.post(url = API_ENDPOINT, json=data, headers=headers)
        returned_data = json.loads(r.text)
        print(returned_data)
        # if response is good send info to frontend
        response = {
            "data": returned_data,
            "message": "GOOD JOB!!! YOU DID THINGS!!!"
        }

        return jsonify(response), 200
    else:
        response = {"message": "YOU SUCK"}
        return jsonify(response), 400

# Players ---------------------------------------------------

# @app.route('/players', methods=['POST'])
# def add_income():
#   incomes.append(request.get_json())
#   return '', 204


if __name__ == "__main__":
    app.run()
