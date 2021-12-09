from threading import Thread


class Broker:
    def __init__(self) -> None:
        self.eventlisteners = set()

    def add_eventlistener(self, eventlistener):
        if eventlistener not in self.eventlisteners:
            self.eventlisteners.add(eventlistener)

    def remove_eventlistener(self, eventlistener):
        if eventlistener in self.eventlisteners:
            self.eventlisteners.remove(eventlistener)

    def router(self, context, topic: str):
        for eventlistener in self.eventlisteners:
            if topic == eventlistener.topic:
                thread = Thread(target=eventlistener.update, args=(context,))
                thread.start()


class Event:
    def __init__(self, broker: Broker, topic: str, context) -> None:
        self.broker = broker
        self.notify(context, topic)

    def notify(self, context, topic: str):
        self.broker.router(context, topic)


class EventListener:
    def __init__(self, broker: Broker, topic: str, callback) -> None:
        broker.add_eventlistener(self)
        self.topic = topic
        self.callback = callback

    def update(self, context):
        self.callback(context)


if __name__ == "__main__":

    broker = Broker()

    EventListener(broker=broker, topic="musica", callback=print)

    Event(broker=broker, topic="musica", context="Do Re Mi")
