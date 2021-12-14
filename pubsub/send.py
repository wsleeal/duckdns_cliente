import json

from redis import Redis

conn = Redis()

conn.publish("*", json.dumps({"topic": "Música", "context": "Do Re Mi11"}))
