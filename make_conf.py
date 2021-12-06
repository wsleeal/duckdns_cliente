import json
import os
import sys
from pathlib import Path

if __name__ == "__main__":  # pragma: no cover

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        path = Path(sys.executable).parent
        duck_ext = "duckdns.exe"
    else:
        path = Path(__file__).parent
        duck_ext = "duckdns.py"

    if not os.path.isfile(Path(path, "config.json")):
        duck_conf = {}
        duck_conf["domain"] = input("Domain: ")
        duck_conf["token"] = input("Token: ")
        duck_conf["delay"] = int(input("Delay (em segundos): "))
        with open(Path(path, "config.json"), "w") as conf:
            json.dump(duck_conf, conf, indent=4)
        os.startfile(Path(path, duck_conf))
