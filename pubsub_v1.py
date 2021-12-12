from abc import ABC, abstractmethod
from threading import Thread
from typing import Dict, Set


class EventHandler(ABC):
    @abstractmethod
    def update(self):
        raise ValueError("Not Implemented")


class __Event:
    def __init__(self) -> None:
        self.event_listeners: Dict[str, Set[EventHandler]] = dict()

    def add_handler(self, topic: str, handler: EventHandler):
        if topic in self.event_listeners:
            self.event_listeners[topic].add(handler)
        else:
            self.event_listeners[topic] = {handler}

    def notify(self, topic: str, context):
        if topic in self.event_listeners:
            for handler in self.event_listeners[topic]:
                thread = Thread(target=handler.update, args=(context,))
                thread.start()


event = __Event()

if __name__ == "__main__":

    class TestHandler(EventHandler):
        def update(self, msg):
            print(msg)

    event.add_handler("msg1", TestHandler())

    event.notify("msg1", "oi")
