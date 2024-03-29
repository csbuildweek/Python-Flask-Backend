import pymongo
import json
import requests
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from graph import Graph

# .ENV
from dotenv import load_dotenv
load_dotenv()

TOKEN1 = os.getenv('TOKEN1')
MONGO_USER1 = os.getenv('MONGO_USER1')
MONGO_PW1 = os.getenv('MONGO_PW1')

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

class Player:
    def __init__(self, token, user, pw):
        self.items = []
        self.cooldown = 0
        self.name = ''
        self.token = token
        self.user = user
        self.pw = pw
        self.graph = Graph()

# CREATE PLAYER
player1 = Player(TOKEN1, MONGO_USER1, MONGO_PW1)
player1.graph.initialize()

# ======== MongoDB Setup ========= #
myclient = pymongo.MongoClient(
    f"mongodb+srv://{MONGO_USER1}:{MONGO_PW1}@treasureseeker-b4iam.mongodb.net/test?retryWrites=true&w=majority")

mydb = myclient["treasuretracker"]
mycol = mydb["map"]


# Map ---------------------------------------------------
@app.route("/", methods=['GET'])
def index():
    return "API Running"

# TODO: make this work for multiple players in the url
@app.route("/player1", methods=['GET'])
def create_player():
    # ======== Creating Map ========= #
    player1.graph.initialize()
    return "API Running"

# # TODO: make this work for multiple players based on the url
# @app.route("/player1/dungeon_crawl", methods=['GET'])
# def dungeon_crawl():
#     # ======== auto run player through map ========= #
#     crawl = True
#     count = 0
#     # cooldown timer
#     cooldown = 0

#     while crawl:
#         print(count)
#         if count > 5:
#             crawl = False
#         count += 1
#         # move player
#         # check cooldown
#         # set timeout
#         # check for items at location
#         # print items at location
#         # if items:
#             # loop through items
#                 # pickup item
#         # if over encombered   # STRETCH
#             # drop items until not over encumbered
#         #

# @app.route('/move')
@app.route('/move', methods=["POST"])
def move_player():
    # send request to lambda server with direction
    direction = request.get_json()['direction']
    print("step1 get direction from frontend: ", direction)
    if direction in player1.graph.current_room.exits.keys(): # {'n': 63, 's': 70}
        print("step2 if check line 71: ", True)
        # Send movement to Lambda Server
        API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
        headers = {
            "Authorization": f'token {TOKEN1}'
        }
        data = {'direction': direction}
        r = requests.post(url=API_ENDPOINT, json=data, headers=headers)
        # room data
        print("RESPONSE: ", r)
        room = json.loads(r.text)
        print("LOOK FOR THIS ONE: ", room)
        # Send room data to graph
        player1.graph.update_map(room, direction)
        # if response is good send info to frontend
        room['adjacent_rooms'] = player1.graph.current_room.exits
        room['message'] = "Movement Good"
        response = {
            "data": room,
        }
        return jsonify(response), 200# TODO: make this work for multiple players based on the url
# @app.route("/player1/dungeon_crawl", methods=['GET'])
# def dungeon_crawl():
#     # ======== auto run player through map ========= #
#     crawl = True
#     count = 0
#     # cooldown timer
#     cooldown = 0

#     while crawl:
#         print(count)
#         if count > 5:
#             crawl = False
#         count += 1
#         # move player
#         # check cooldown
#         # set timeout
#         # check for items at location
#         # print items at location
#         # if items:
#             # loop through items
#                 # pickup item
#         # if over encombered   # STRETCH
#             # drop items until not over encumbered
#         #
    else:
        # raise TypeError
        print("ERROR Direction: ", direction)
        # response = {"data": f"Can't go {direction}"}
        response = {}
        response['data'] = {"message": f"Error: Can't go in that direction"}
        return jsonify(response), 400


# @app.route('/take')
@app.route('/take', methods=["POST"])
def take_item():
    name = request.get_json()['name']
    API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/'
    headers = {
        "Authorization": f'token {TOKEN1}'
    }
    data = {'name': name}
    print('Name: ', data)
    r = requests.post(url=API_ENDPOINT, json=data, headers=headers)
    returned_data = json.loads(r.text)
    print(returned_data)
    # if response is good send info to frontend
    response = {
        "data": returned_data,
    }

    return jsonify(response), 200

# @app.route('/drop')
@app.route('/drop', methods=["POST"])
def drop_item():
    name = request.get_json()['name']
    API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/'
    headers = {
        "Authorization": f'token {TOKEN1}'
    }
    data = {'name': name}
    print('Name: ', data)
    r = requests.post(url=API_ENDPOINT, json=data, headers=headers)
    returned_data = json.loads(r.text)
    print(returned_data)
    # if response is good send info to frontend
    response = {
        "data": returned_data,
    }

    return jsonify(response), 200

# @app.route('/sell')
@app.route('/sell', methods=["POST"])
def sell_item():
    name = request.get_json()['name']
    API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/'
    headers = {
        "Authorization": f'token {TOKEN1}'
    }
    data = {'name': name, "confirm": "yes"}
    print('Name: ', data)
    r = requests.post(url=API_ENDPOINT, json=data, headers=headers)
    returned_data = json.loads(r.text)
    print(returned_data)
    # if response is good send info to frontend
    response = {
        "data": returned_data,
    }

    return jsonify(response), 200

# @app.route('/status')
@app.route('/status', methods=["POST"])
def check_status():
    API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/'
    headers = {
        "Authorization": f'token {TOKEN1}'
    }

    r = requests.post(url=API_ENDPOINT, headers=headers)
    returned_data = json.loads(r.text)
    print(returned_data)
    # if response is good send info to frontend
    response = {
        "data": returned_data,
    }

    return jsonify(response), 200

# @app.route('/examine')
@app.route('/examine', methods=["POST"])
def examine():
    name = request.get_json()['name']
    API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/'
    headers = {
        "Authorization": f'token {TOKEN1}'
    }
    data = {'name': name}
    print('Name: ', data)
    r = requests.post(url=API_ENDPOINT, json=data, headers=headers)
    returned_data = json.loads(r.text)
    print(returned_data)
    # if response is good send info to frontend
    response = {
        "data": returned_data,
    }

    return jsonify(response), 200

# @app.route('/change_name')
@app.route('/change_name', methods=["POST"])
def name_change():
    name = request.get_json()['name']
    API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/'
    headers = {
        "Authorization": f'token {TOKEN1}'
    }
    data = {'name': name, 'confirm': "aye"}
    print('Name: ', data)
    r = requests.post(url=API_ENDPOINT, json=data, headers=headers)
    returned_data = json.loads(r.text)
    print(returned_data)
    # if response is good send info to frontend
    response = {
        "data": returned_data,
    }

    return jsonify(response), 200

# @app.route('/pray')
@app.route('/pray', methods=["POST"])
def pray():
    API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/'
    headers = {
        "Authorization": f'token {TOKEN1}'
    }
    r = requests.post(url=API_ENDPOINT, headers=headers)
    returned_data = json.loads(r.text)
    print(returned_data)
    # if response is good send info to frontend
    response = {
        "data": returned_data,
    }

    return jsonify(response), 200


# @app.route('/fly')
@app.route('/fly', methods=["POST"])
def fly():
    # send request to lambda server with direction
    direction = request.get_json()['direction']
    print("DIRECTION: ", direction)
    if direction in ['n', 'e', 'w', 's']:
        API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/'
        headers = {
            "Authorization": f'token {TOKEN1}'
        }
        data = {'direction': direction}
        print('DATAAAAAAAAA: ', data)
        r = requests.post(url=API_ENDPOINT, json=data, headers=headers)
        returned_data = json.loads(r.text)
        print(returned_data)
        # if response is good send info to frontend
        response = {
            "data": returned_data,
        }

        return jsonify(response), 200
    else:
        response = {"message": "Error"}
        return jsonify(response), 400


@app.route("/get_balance", methods=['GET'])
def balance():
    API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/'
    headers = {
        "Authorization": f'token {TOKEN1}'
    }

    r = requests.get(url=API_ENDPOINT, headers=headers)
    returned_data = json.loads(r.text)
    response = {
        "data": returned_data,
    }
    return jsonify(response), 200


# Players ---------------------------------------------------
# @app.route('/players', methods=['POST'])
# def add_income():
#   incomes.append(request.get_json())
#   return '', 204
if __name__ == "__main__":
    app.run(debug=True)


# MVP
# Collect 1000 gold
# traverse the map
# Find Pirate Ray and change your name
# Mine at least one Lambda Coin
