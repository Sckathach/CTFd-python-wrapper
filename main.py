from wrapper.client import Client
from wrapper.flag import Flag
from wrapper.challenge import Challenge
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"

client = Client()
# USER_TOKEN = "ctfd_d8bb6f6a5154ad987706c977f0699607e19dae0cc9ed77b75eb011ad3055fc89"
client.setup(URL, TOKEN, verbose="debug")

client.fetch_flags()

print(client.attempt_challenge("flag", 69, 3))


# client.delete_challenges()
# for i in range(100):
#     print(f"Creation chall {i}")
#     x = Challenge.create(f"Bof{i}", "PWN")
#     x = client.add_challenge(x)
#     f = Flag.create("flag", x.id)
#     f = client.add_flag(f)
#     print(f"Chall : {x}")
