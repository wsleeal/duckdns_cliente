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


def event(topic: str):
    def inner(func):
        def wrapper(*args, **kwargs):
            context = func(*args, **kwargs)
            _globals = globals()
            broker_find = 0
            for broker in _globals:
                if isinstance(_globals[broker], Broker):
                    Event(_globals[broker], topic, context)
                    broker_find += 1
                else:
                    continue

            if broker_find == 0:
                raise ValueError("No Broker on Globals")
            else:
                return context

        return wrapper

    return inner


if __name__ == "__main__":

    broker = Broker()

    EventListener(broker=broker, topic="musica", callback=print)

    @event("musica")
    def event_on_call_fuction():
        return "Do Re Mi"

    event_on_call_fuction()

    Event(broker, "musica", "Do Re Mi")
