from dotenv import load_dotenv
import os

ABSOLUTE_PATH = os.path.dirname(__file__)
TOKEN_FILE = ".env"
CONFIG_FILE = ".config"
ROOT_DIR = os.path.join(ABSOLUTE_PATH, "../")

load_dotenv(os.path.join(ROOT_DIR, TOKEN_FILE))
load_dotenv(os.path.join(ROOT_DIR, CONFIG_FILE))

TOKEN = os.getenv("TOKEN")
FULL_VERBOSE = os.getenv("VERBOSE") == "Full"
SIMPLE_VERBOSE = os.getenv("VERBOSE") == "Simple" or os.getenv("VERBOSE") == "Full"
URL = os.getenv("URL")
