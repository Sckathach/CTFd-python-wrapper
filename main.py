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
client.list_challenges()
x = client.challenges["1"]
