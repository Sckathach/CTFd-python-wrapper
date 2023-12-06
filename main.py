from wrapper.client import Client
from dotenv import load_dotenv
from wrapper.flag import Flag
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"

client = Client()
client.setup(URL, TOKEN)

client.fetch_challenges()

x = client.challenges["1"]
f = Flag.create("Test{YOOOOOOOOOOOOo}", x.id)
x.flags = [f]
x.name = "bob2"
client.update_challenge(x)
