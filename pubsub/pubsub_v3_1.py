import json

import faker

from pubsub_v3_0 import Fila

fake = faker.Faker()

fila = Fila("fila")


for n in range(0, 1000):
    context = dict()
    context["1"] = fake.name()
    context["2"] = fake.name()

    fila.set(json.dumps({"topic": "nomes", "context": context}))
