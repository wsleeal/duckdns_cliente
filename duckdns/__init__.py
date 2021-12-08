import datetime
import os
from pathlib import Path
from tkinter import messagebox

import pystray
from PIL import Image, ImageTk
from pystray import MenuItem as item

from .main import DuckConfig, DuckDNS, Logger


class SysTray:
    def __init__(self) -> None:

        self.file_path = Path(__file__).parent
        logger = Logger(name="DuckDNS").get_logger()
        config = DuckConfig()
        self.ddns = DuckDNS(domain=config.domain, token=config.token, delay=config.delay, logger=logger)

    def quit_window(self, icon):
        self.ddns.stop()
        icon.stop()

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
        menu = (pystray.MenuItem("Log", self.open_log), pystray.MenuItem("Quit", self.quit_window))
        icon = pystray.Icon("name", image, "My System Tray Icon", menu)
        self.ddns.start()
        icon.run()


def show():
    systray = SysTray()
    systray.start()
