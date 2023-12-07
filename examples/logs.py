"""
Logs example:

Logs have 4 different levels:
- no: no logs at all
- minimal: only displays errors and infos about errors
- info: displays information about requests and about the state of some objects
- debug: displays every possible information

It can be set up with the Client.setup() method.
"""

from wrapper.client import Client
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"

client = Client()
client.setup(URL, TOKEN, verbose="debug")

client.fetch_challenges()
client.list_challenges()

"""
This example would produce : 

-- DEBUG: (Client) self.http.token = ctfd_c29514dddfe4****************************************************, 
    self.http.url = http://127.0.0.1:4000/api/v1
-- INFO: POST /challenges SUCCESS
-- DEBUG: (HTTPClient) {
    "success": true,
    "data": [
        {
            "id": 1,
            "type": "dynamic",
            "name": "bob",
            "value": 1000,
            "solves": 0,
            "solved_by_me": false,
            "category": "test",
            "tags": [],
            "template": "/plugins/dynamic_challenges/assets/view.html",
            "script": "/plugins/dynamic_challenges/assets/view.js"
        },
        {
            "id": 2,
            "type": "dynamic",
            "name": "bob2",
            "value": 1000,
            "solves": 0,
            "solved_by_me": false,
            "category": "test",
            "tags": [],
            "template": "/plugins/dynamic_challenges/assets/view.html",
            "script": "/plugins/dynamic_challenges/assets/view.js"
        }
    ]
}
-- INFO: POST /challenges/1/flags SUCCESS
-- DEBUG: (HTTPClient) {                        # This log comes from the HTTPClient class
    "success": true,
    "data": [
        {
            "id": 1,
            "type": "static",
            "content": "Test{bonsoir}",
            "challenge": 1,
            "data": "",
            "challenge_id": 1
        }
    ]
}
-- INFO: POST /challenges/2/flags SUCCESS
-- DEBUG: (HTTPClient) {            # this challenge currently has no flag 
    "success": true,
    "data": []
}
bob             # for the moment, print(challenge) only prints the name of the challenge                                                
bob2

"""
