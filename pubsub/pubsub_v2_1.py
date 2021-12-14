from abc import ABC, abstractmethod
from typing import Dict, Set


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
