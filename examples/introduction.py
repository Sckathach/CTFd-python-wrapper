from wrapper.challenge import Challenge
from wrapper.client import Client

# Imports to use .env files
from dotenv import load_dotenv
import os

# Load .env, use load_dotenv("<config>") to load file with name <config>
load_dotenv()

# Get the .env variables
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"

# Set up the Client
client = Client()
client.setup(URL, TOKEN)

# Create a simple challenge
chall = Challenge.create("bob", "test")

# Add the challenge to the Client, it will be automatically pushed to the CTFd instance
client.add_challenge(chall)
