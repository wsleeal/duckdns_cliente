import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from threading import Lock, Thread

import requests
from pytz import timezone


class Logger:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def formater(self):
        msg_formater = "%(asctime)s - %(levelname)s - %(message)s"
        date_formater = "%d/%m/%Y, %H:%M:%S"
        formater = logging.Formatter(msg_formater, date_formater)
        return formater

    def stream_handler(self):
        stream_handler = logging.StreamHandler()
        formater = self.formater()
        stream_handler.setFormatter(formater)
        return stream_handler

    def file_handler(self):
        log_path = Path(Path(self.file_path), "logs")
        if not os.path.isdir(log_path):
            os.makedirs(log_path)
        hoje = datetime.now().strftime("%d-%m-%Y")
        log_file = Path(log_path, f"{hoje}.log")
        file_handler = logging.FileHandler(log_file)
        formater = self.formater()
        file_handler.setFormatter(formater)
        return file_handler

    def get_logger(self, name: str = None):
        logger = logging.getLogger(name)
        stream_handler = self.stream_handler()
        logger.addHandler(stream_handler)
        file_handler = self.file_handler()
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger


class DuckDNS:

    stopped = False
    lock = None

    def __init__(self, domain: str, token: str, delay: int, logger=None) -> None:
        self.domain = domain
        self.token = token
        self.delay = delay
        self.logger = logger or logging.root
        self.lock = Lock()

    @property
    def timestamp(self) -> float:
        return time.time()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.lock.acquire()
        self.stopped = True
        self.lock.release()

    def timestamp_to_hour(self, timestamp: float) -> str:
        hora = datetime.fromtimestamp(timestamp, tz=timezone("America/Sao_Paulo"))
        hora = hora.strftime("%H:%M:%S")
        return hora

    def run(self):
        last_check = 0
        while not self.stopped:
            if (self.timestamp - last_check) > self.delay:
                last_check = self.timestamp

                try:
                    url = "https://www.duckdns.org/update?domains={}&token={}&ip="
                    response = requests.get(url.format(self.domain, self.token))
                except:
                    self.logger.exception("Request Error")
                    time.sleep(self.delay)

                if response.status_code == 200:
                    hora = self.timestamp_to_hour(last_check + self.delay)
                    self.logger.info(f"Resposta: {response.text}, Proxima Checagem: {hora}")
            time.sleep(0.1)


class DuckConfig:
    def __init__(self) -> None:

        self.path = Path(__file__).parent

        self.domain = self.get_config_var("domain")
        self.token = self.get_config_var("token")
        self.delay = self.get_config_var("delay")

    def get_config_var(self, var: str):
        if os.path.isfile(Path(self.path, "config.json")):
            with open(Path(self.path, "config.json")) as f:
                data: dict = json.load(f)
                return data.get(var)
        else:
            duck_conf = {}
            duck_conf["domain"] = self.domain = input("Domain: ")
            duck_conf["token"] = self.token = input("Token: ")
            duck_conf["delay"] = self.delay = int(input("Delay (em segundos): "))
            with open(Path(self.path, "config.json"), "w") as conf:
                json.dump(duck_conf, conf, indent=4)
