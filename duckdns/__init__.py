from .main import SysTray


def show():
    systray = SysTray()
    systray.start()
