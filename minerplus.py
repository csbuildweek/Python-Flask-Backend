import requests
import os
import os.path
import hashlib
import json
import time
import random

from dotenv import load_dotenv
load_dotenv()

TOKEN1 = os.getenv('TOKEN1')
MONGO_USER1 = os.getenv('MONGO_USER1')
MONGO_PW1 = os.getenv('MONGO_PW1')

class Miner:
    def __init__(self):
        self.proof = 0
        self.last_proof = ''
        self.difficulty = 8
        self.cooldown = 1

    def get_proof(self):
        API_ENDPOINT = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/'
        headers = {"Authorization": f'token {TOKEN1}'}
        r = requests.get(url=API_ENDPOINT, headers=headers)
        last_proof = json.loads(r.text)
        print("LAST PROOF: ", last_proof)
        self.last_proof = last_proof['proof']
        self.proof = last_proof['proof']
        self.difficulty = last_proof['difficulty'] 
        self.cooldown = last_proof['cooldown']


    def proof_of_work(self):
        print("Searching for next proof")
        self.proof = self.last_proof
        while self.valid_proof() is False:
            self.proof += 1
        print(f"Proof found: {self.proof}")
        
        return self.proof

    def valid_proof(self):
        guess = f'{self.last_proof}{self.proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == '0' * self.difficulty

miner = Miner()



while True:
    miner.get_proof()
    time.sleep(miner.cooldown)
    miner.proof_of_work()
    # send found proof to lambda server
    headers = {"Authorization": 'Token 9a7bff2905601b94f7900f314cb4d4c930bbe025'}
    r = requests.post(url="https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/", json={"proof": f"{miner.proof}"}, headers=headers)
    response = json.dumps(r.text)
    print(response['cooldown'])
    time.sleep(miner.cooldown)