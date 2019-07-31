from util import Stack, Queue
from flask import Flask, jsonify, request
import pymongo
import json
import requests
import os
import time

from dotenv import load_dotenv
load_dotenv()

TOKEN1 = os.getenv('TOKEN1')
MONGO_USER1 = os.getenv('MONGO_USER1')
MONGO_PW1 = os.getenv('MONGO_PW1')

# ===================================== MONGODB SETUP ===================================== #
# import pymongo
# myclient = pymongo.MongoClient(
#     f"mongodb+srv://{MONGO_USER1}:{MONGO_PW1}@treasureseeker-b4iam.mongodb.net/test?retryWrites=true&w=majority")

# mydb = myclient["treasuretracker"]
# mycol = mydb["map"]

# print(myclient.list_database_names())


class Room:
    def __init__(self, id, title, description, coordinates, exits, elevation, terrain, items, players):
        self.id = id
        self.title = title
        self.description = description
        self.coordinates = coordinates
        self.elevation = elevation
        self.terrain = terrain
        self.exits = exits
        self.items = items
        self.players = players

class Graph:
    def __init__(self):
        self.map = {}
        self.current_room = None
        self.prev_room = None
        self.coordinates = [60, 60]
        self.traversal_path = []
        self.visited_rooms = ()
        self.shop_coordinates = [59,60]
        self.cooldown = 0

    def initialize(self):

        
        API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
        headers = {
            "Authorization": f'token {TOKEN1}'
        }
        r = requests.get(url = API_ENDPOINT, headers=headers)
        room = json.loads(r.text)
        print("Init ROOM: ", room)
        if len(room['errors']) == 0:
            id = room['room_id']
            exits = {}
            for i in room['exits']:
                exits[i] = ''
            print(exits)
            self.map[id] = Room(room['room_id'], room['title'], room['description'], room['coordinates'], exits, room['elevation'], room['terrain'], room['items'], room['players'])
            self.current_room = self.map[id]
            print("CURRENT_ROOM", self.map[id])
            self.cooldown = room['cooldown']
            print("current Room ID: ", self.current_room.id)
            print("current Room Title: ", self.current_room.title)
            print("current Room Cooldown: ", self.cooldown)

    def update_map(self, room, direction):
        print("UPDATE")
        print("ROOM: ", room)
        print("COOLDOWN : ", self.cooldown)
        if len(room['errors']) == 0:
            id = room['room_id']
            self.cooldown = room['cooldown']
            if id not in self.map:
                print("NEW ROOM")
                exits = {}
                for i in room['exits']:
                    exits[i] = ''
                print(exits)
                # create new room node
                self.map[id] = Room(room['room_id'], room['title'], room['description'], room['coordinates'], exits, room['elevation'], room['terrain'], room['items'], room['players'])
                self.prev_room = self.current_room
                self.current_room = self.map[id]
                self.prev_room.exits[direction] = id
                if direction == 'n':
                    opp_direction = 's'
                elif direction == 's':
                    opp_direction = 'n'
                elif direction == 'e':
                    opp_direction = 'w'
                elif direction == 'w':
                    opp_direction = 'e'
                self.current_room.exits[opp_direction] = self.prev_room.id
                print("CURRENT ROOM EXITS: ", self.current_room.exits)
                print("PREV ROOM EXITS: ", self.prev_room.exits)






# ========================================== TEMPORARY SECTION ========================================== #
# graph = Graph()

# graph.initialize()
# print("EXITS: ", graph.current_room.exits)

# def move_player(direction):
#     print("CURRENT ROOM EXITS: ", graph.current_room.exits)
#     if direction in graph.current_room.exits.keys():
#         API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
#         headers = {
#             "Authorization": f'token {TOKEN1}'
#         }
#         data = {'direction': direction}
#         # print('DATAAAAAAAAA: ', data)
#         r = requests.post(url = API_ENDPOINT, json=data, headers=headers)
#         room = json.loads(r.text)
#         # print(room)
#         graph.update_map(room, direction)
#     else:
#         print("DENIED: CAN'T GO THAT WAY!")


# print("COOLDOWN: ", graph.cooldown)
# time.sleep(int(graph.cooldown))

# print("===================================================================================================================================")
# move_player('n')
# print("COOLDOWN: ", graph.cooldown)

# print("===================================================================================================================================")
# move_player('s')
# print("COOLDOWN: ", graph.cooldown)