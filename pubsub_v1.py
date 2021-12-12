from typing import Callable, Dict, Set


class __Event:
    def __init__(self) -> None:
        self.event_listeners: Dict[str, Set[Callable[[str], None]]] = dict()

    def add_listener(self, topic: str, callback: Callable[[str], None]):
        if topic in self.event_listeners:
            self.event_listeners[topic].add(callback)
        else:
            self.event_listeners[topic] = {callback}

    def notify(self, topic: str, context: str):
        if topic in self.event_listeners:
            for callback in self.event_listeners[topic]:
                callback(context)


Event = __Event()

if __name__ == "__main__":

    Event.add_listener("msg1", print)

    Event.notify("msg1", "oi")
