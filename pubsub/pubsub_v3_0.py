import json
import random
import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Set

import redis


class Fila:
    def __init__(self, pattern: str) -> None:
        self.redis = redis.Redis(host="127.0.0.1", port=6379, db=0)
        self.pattern = pattern

    def get_keys(self):
        # Get all keys from pattern
        return self.redis.keys(f"{self.pattern}:*")

    def get(self, key: str):
        # Get Value of key
        valor = self.redis.get(key)
        return self._parse(valor)

    def set(self, valor: str, ttl: int = None):
        # Set value and ttl
        key = uuid.uuid4()
        return self.redis.set(f"{self.pattern}:{str(key)}", valor, ttl)

    def delete(self, key: str):
        # Delete key
        return self.redis.delete(key)

    def _parse(self, valor):
        # parse value for utf-8
        if isinstance(valor, bytes):
            return bytes(valor).decode("utf-8")
        return valor


class EventListener(ABC):
    @abstractmethod
    def update(self, context):
        raise ValueError("Not Implemented")


class Broker:
    def __init__(self) -> None:
        self.event_listeners: Dict[str, Set[EventListener]] = dict()

    def add_event_listener(self, topic: str, event_listener: EventListener):
        if topic in self.event_listeners:
            self.event_listeners[topic].add(event_listener)
        else:
            self.event_listeners[topic] = {event_listener}

    def notify(self, topic: str, context):
        if topic in self.event_listeners:
            for listener in self.event_listeners[topic]:
                listener.update(context)
            return True
        return False


class PubSub(Broker):
    def __init__(self) -> None:
        super().__init__()
        self.fila = Fila("fila")

    def run_fila(self):
        for key in self.fila.get_keys():
            values = self.fila.get(key)
            values = json.loads(values)

            values_parsed = dict()
            for k in values:
                if isinstance(values[k], bytes):
                    values_parsed[k] = bytes(values[k]).decode("utf-8")
                else:
                    values_parsed[k] = values[k]

            topic = values_parsed["topic"] if "topic" in values_parsed else None
            context = values_parsed["context"] if "context" in values_parsed else None

            if self.notify(topic, context):
                self.fila.delete(key)
        time.sleep(1)


if __name__ == "__main__":

    class ListenerTeste(EventListener):
        def update(self, context):
            print(context)

    pubsub = PubSub()
    pubsub.add_event_listener("nomes", ListenerTeste())

    while True:
        pubsub.run_fila()
        time.sleep(0.1)
