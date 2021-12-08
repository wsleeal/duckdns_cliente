# Import the required libraries
import datetime
import os
from pathlib import Path
from tkinter import messagebox

import pystray
from PIL import Image

from main import DuckConfig, DuckDNS, Logger

file_path = Path(__file__).parent
logger = Logger(name="DuckDNS").get_logger()
config = DuckConfig()
ddns = DuckDNS(domain=config.domain, token=config.token, delay=config.delay, logger=logger)
ddns.start()


def quit_window(icon):
    icon.stop()
    ddns.stop()


def open_log():
    hoje = datetime.datetime.now().strftime("%d-%m-%Y")
    log_path = Path(Path(file_path), "logs", f"{hoje}.log")
    if os.path.isfile(log_path):
        os.startfile(log_path)
    else:
        messagebox.showinfo("DuckDNS", "Log não encontrado !")


def show():
    favicon = Path(file_path, "favicon.ico")
    image = Image.open(favicon)
    menu = (pystray.MenuItem("Log", open_log), pystray.MenuItem("Quit", quit_window))
    icon = pystray.Icon("name", image, "My System Tray Icon", menu)
    icon.run()
