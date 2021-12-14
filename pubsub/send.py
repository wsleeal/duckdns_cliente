import json

from redis import Redis

conn = Redis()

msg = dict()
msg["nome"] = "Leal"
msg["sobrenome"] = "Leal"

for n in range(500000000):

    msg["count"] = n
    conn.publish("teste", json.dumps(msg))
