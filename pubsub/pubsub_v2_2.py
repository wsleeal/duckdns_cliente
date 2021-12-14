from redis import StrictRedis

from pubsub_v2_1 import Broker, EventListener


class TesteBroker(EventListener):
    def update(self, context):
        print(context)


class PubSub(Broker):

    stopped = None

    def __init__(self) -> None:
        super().__init__()

        client = StrictRedis(host="localhost", port=6379)

        self.subscriber = client.pubsub()
        self.subscriber.psubscribe(**{"*": self.event_handler})

    def start(self):
        self.stopped = False
        self.thread = self.subscriber.run_in_thread(sleep_time=0.01)

    def stop(self):
        if not self.stopped:
            self.thread.stop()

    def event_handler(self, msg):
        msg_parsed = dict()
        for k in msg:
            if isinstance(msg[k], bytes):
                msg_parsed[k] = bytes(msg[k]).decode("utf-8")
            else:
                msg_parsed[k] = msg[k]
        topic = msg_parsed["channel"] if "channel" in msg_parsed else None
        context = msg_parsed["data"] if "data" in msg_parsed else None
        self.notify(topic, context)


if __name__ == "__main__":

    broker = PubSub()

    broker.add_event_listener("teste", TesteBroker())

    try:
        while True:
            ...
    except KeyboardInterrupt:
        broker.stop()
