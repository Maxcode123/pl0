import os
from pathlib import Path

from lectes import Configuration, Scanner

config_path = Path(os.path.realpath(os.path.dirname(__file__))) / Path("config.lectes")

with open(config_path, "r") as f:
    config = Configuration.from_text(f.read())

scanner = Scanner(config)
scanner.ignore("WHITESPACE")
