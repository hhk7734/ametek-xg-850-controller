import PyInstaller.__main__
from os import path

BASE_DIR = path.dirname(__file__)

PyInstaller.__main__.run(
    [
        "--name=XG-850-controller",
        "--windowed",
        "--onefile",
        "--icon={}".format(path.join(BASE_DIR, "img/Ametek.ico")),
        "main.py",
    ]
)
