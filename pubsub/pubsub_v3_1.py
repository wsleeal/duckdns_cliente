import json

import faker

from pubsub_v3_0 import Fila

fake = faker.Faker()

fila = Fila("fila")


for n in range(0, 1000):

    fila.set("nomes", (fake.name(), fake.name()))

    # for key in fila.get_keys():
    #     fila.delete(key)

fila.redis.close()
