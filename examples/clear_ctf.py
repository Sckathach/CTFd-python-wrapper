from wrapper.client import Client
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"

client = Client()
client.setup(URL, TOKEN, verbose="debug")

# Fetch everything
client.fetch_flags()
client.fetch_challenges()
client.fetch_users()

# Delete everything
client.delete_users()
client.delete_flags()
client.delete_challenges()
