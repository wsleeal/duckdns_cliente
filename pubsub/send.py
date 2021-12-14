import json
import time

from redis import Redis

conn = Redis()

msg = dict()
msg["nome"] = "Leal"
msg["sobrenome"] = "Leal"

inicio = time.time()

for n in range(5000):

    msg["count"] = n
    conn.publish("teste", json.dumps(msg))

termino = time.time() - inicio
print(int(termino))
