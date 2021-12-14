import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Set

from redis import StrictRedis


class EventListener(ABC):
    @abstractmethod
    def update(self):
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
            for handler in self.event_listeners[topic]:
                handler.update(context)


def event_handler(msg):
    try:
        data = json.loads(msg["data"])
    except:
        data = {}

    topic = data["topic"] if "topic" in data else None
    context = data["context"] if "context" in data else None
    broker = Broker()
    broker.notify(topic, context)


client = StrictRedis(host="localhost", port=6379)

subscriber = client.pubsub()
subscriber.psubscribe(**{"*": event_handler})

thr = subscriber.run_in_thread(sleep_time=0.01)
try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    thr.stop()
