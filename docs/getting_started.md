# Getting started

First, import everything needed:

```python
from wrapper.challenge import Challenge
from wrapper.client import Client

# Imports to use .env files.
from dotenv import load_dotenv
import os

# Load .env, use load_dotenv("<config>") to load file with name <config>.
load_dotenv()

# Get the .env variables.
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"
```

Every operation on the CTFd instance has to be taken from a client object that contains the TOKEN and the URL. It can be
initiated at the beginning of the script:

```python
client = Client()
client.setup(URL, TOKEN)
```

```{attention}
Every object is stored locally and on the CTFd instance. It will be possible in the future to keep only one instance
of each object. For the moment, it was designed to make extensive queries locally without having to request the CTFd
instance.
```

To create a instance of an object locally, the easiest way is to call the `.create()` method. It works for
`Challenge`, `User`, `Flag`, and `Token`:

```python
chall = Challenge.create("bob", "test")
```

When the instance of the object is created locally, it does not yet have an ID. So the default value is set to -1. To
have an ID, the object has to be sent to the CTFd instance:

```python
chall = client.add_challenge(chall)
```

The `chall.id` will then be updated.
