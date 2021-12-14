from pubsub_v2_2 import EventListener, PubSub


class TesteBroker(EventListener):
    def update(self, context):
        print(context)


broker = PubSub()

broker.add_event_listener("teste", TesteBroker())

broker.start()

try:
    while True:
        ...
except KeyboardInterrupt:
    broker.stop()
