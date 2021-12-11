from threading import Thread
from typing import Any, Dict, List, Set


class Broker:
    def __init__(self) -> None:
        self.eventlisteners: Dict[str, EventListener] = dict()
        self.fila_de_eventos: Set[List[str, Any]] = set()

    def add_eventlistener(self, topic, eventlistener):
        if topic in self.eventlisteners:
            self.eventlisteners[topic].add(eventlistener)
        else:
            self.eventlisteners[topic] = {eventlistener}

    def add_event(self, topic: str, context: Any):
        self.fila_de_eventos.add((topic, context))

    def router(self, topic: str, context: Any):
        for eventlistener in self.eventlisteners[topic]:
            thread = Thread(target=eventlistener.update, args=(context,))
            thread.start()

    def broadcast(self):
        for topic, context in self.fila_de_eventos:
            self.router(topic, context)
        self.fila_de_eventos.clear()


class EventListener:
    def __init__(self, broker: Broker, topic: str, callback) -> None:
        broker.add_eventlistener(topic, self)
        self.callback = callback

    def update(self, context):
        self.callback(context)


if __name__ == "__main__":

    broker = Broker()

    EventListener(broker=broker, topic="musica", callback=print)

    broker.add_event(topic="musica", context="Do Re Mi")

    broker.broadcast()
