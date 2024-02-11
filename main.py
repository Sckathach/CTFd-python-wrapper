from simulation import Simulation
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:8000/api/v1"

simulation = Simulation(TOKEN, URL)
simulation.run_simple_gaussian_uniform(interval=0.2)
