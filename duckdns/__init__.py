# Import the required libraries
import datetime
import os
import tkinter
from pathlib import Path
from tkinter import *
from tkinter import messagebox

import pystray
from PIL import Image
from pystray import MenuItem as item

win = Tk()


def quit_window(icon):
    icon.stop()
    win.destroy()


def open_log():
    aqui = Path(__file__).parent
    hoje = datetime.datetime.now().strftime("%d-%m-%Y")
    log_path = Path(Path(aqui), "logs", f"{hoje}.log")
    if os.path.isfile(log_path):
        os.startfile(log_path)
    else:
        messagebox.showinfo("DuckDNS", "Log não encontrado !")


def show():
    win.withdraw()
    image = Image.open("favicon.ico")
    menu = (item("Log", open_log), item("Quit", quit_window))
    icon = pystray.Icon("name", image, "My System Tray Icon", menu)
    icon.run()


show()
