import datetime
import json
import logging
import os
import time
from pathlib import Path
from threading import Lock, Thread
from tkinter import messagebox

import pystray
import requests
from PIL import Image
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
        hoje = datetime.datetime.now().strftime("%d-%m-%Y")
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
        hora = datetime.datetime.fromtimestamp(timestamp, tz=timezone("America/Sao_Paulo"))
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
        config_path = Path(self.path, "config.json")
        if os.path.isfile(config_path):
            with open(config_path) as f:
                data: dict = json.load(f)
                try:
                    return data.get(var)
                except:
                    os.remove(config_path)
                    self.make_config()
        else:
            self.make_config()

    def make_config(self):
        duck_conf = {}
        duck_conf["domain"] = self.domain = input("Domain: ")
        duck_conf["token"] = self.token = input("Token: ")
        duck_conf["delay"] = self.delay = int(input("Delay (em segundos): "))
        with open(Path(self.path, "config.json"), "w") as conf:
            json.dump(duck_conf, conf, indent=4)


class SysTray:
    def __init__(self) -> None:

        self.file_path = Path(__file__).parent
        logger = Logger(self.file_path).get_logger("DuckDNS")
        config = DuckConfig()
        self.ddns = DuckDNS(domain=config.domain, token=config.token, delay=config.delay, logger=logger)

    def quit_window(self, icon):
        self.ddns.stop()
        icon.stop()

    def open_config(self):
        config_path = Path(Path(self.file_path), "config.json")
        if os.path.isfile(config_path):
            os.startfile(config_path)
        else:
            messagebox.showinfo("DuckDNS", "Config não encontrado !")

    def open_log(self):
        hoje = datetime.datetime.now().strftime("%d-%m-%Y")
        log_path = Path(Path(self.file_path), "logs", f"{hoje}.log")
        if os.path.isfile(log_path):
            os.startfile(log_path)
        else:
            messagebox.showinfo("DuckDNS", "Log não encontrado !")

    def start(self):
        favicon = Path(self.file_path, "favicon.ico")
        image = Image.open(favicon)
        menu = pystray.Menu(
            pystray.MenuItem("Config", self.open_config),
            pystray.MenuItem("Log", self.open_log, default=True),
            pystray.MenuItem("Quit", self.quit_window),
        )
        icon = pystray.Icon("name", image, "DuckDNS", menu)
        self.ddns.start()
        icon.run()
