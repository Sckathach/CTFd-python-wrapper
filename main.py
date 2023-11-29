from wrapper.challenge import *


TOKEN = "ctfd_c29514dddfe408e78771233e5b6c927640c97a1702ed6d9267ed3d9d8961bce9"
URL = "http://localhost:4000/api/v1"

setup(TOKEN, URL)

x = Challenge.create("bonsoir", "fatigué")
x.push()
