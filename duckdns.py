import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path

import requests
from pytz import timezone


class Logger:
    def __init__(self, file_path: str, name: str) -> None:
        self.file_path = file_path
        self.name = name

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
        name = self.name if name is None else name
        logger = logging.getLogger(name)
        stream_handler = self.stream_handler()
        logger.addHandler(stream_handler)
        file_handler = self.file_handler()
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger


class DuckDNS:
    def __init__(self, domain: str, token: str, delay: int, logger=None) -> None:
        self.domain = domain
        self.token = token
        self.delay = delay
        self.logger = logger or logging.root

    @property
    def timestamp(self) -> float:
        return time.time()

    def timestamp_to_hour(self, timestamp: float) -> str:
        hora = datetime.fromtimestamp(timestamp, tz=timezone("America/Sao_Paulo"))
        hora = hora.strftime("%H:%M:%S")
        return hora

    def start(self, no_loop=False, api_url: str = None):
        last_check = 0
        while True:
            if (self.timestamp - last_check) > self.delay:
                last_check = self.timestamp

                try:
                    url = "https://www.duckdns.org/update?domains={}&token={}&ip="
                    url = url if api_url is None else api_url
                    response = requests.get(url.format(self.domain, self.token))
                except:
                    self.logger.exception("Request Error")
                    time.sleep(self.delay)

                if response.status_code == 200:
                    hora = self.timestamp_to_hour(last_check + self.delay)
                    self.logger.info(f"Resposta: {response.text}, Proxima Checagem: {hora}")
            time.sleep(0.1)
            if no_loop:
                break


if __name__ == "__main__":  # pragma: no cover
    path = Path(__file__).parent
    logger = Logger(file_path=path, name="DuckDNS")
    logger = logger.get_logger()
    if not os.path.isfile(Path(path, "config.json")):
        duck_conf = {}
        duck_conf["domain"] = domain = input("Domain: ")
        duck_conf["token"] = token = input("Token: ")
        duck_conf["delay"] = delay = int(input("Delay (em segundos): "))
        with open(Path(path, "config.json"), "w") as conf:
            json.dump(duck_conf, conf, indent=4)
    else:
        with open(Path(path, "config.json")) as f:
            data = json.load(f)
            domain = data["domain"]
            token = data["token"]
            delay = data["delay"]

    dynamic_dns = DuckDNS(domain=domain, token=token, delay=delay, logger=logger)
    dynamic_dns.start()
