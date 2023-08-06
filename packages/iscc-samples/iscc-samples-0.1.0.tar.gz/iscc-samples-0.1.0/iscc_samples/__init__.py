__version__ = "0.1.0"
from pathlib import Path
from os.path import realpath, dirname

HERE = Path(dirname(realpath(__file__)))
ROOT = HERE / "files"
TEXT = ROOT / "text"
IMAGE = ROOT / "image"
AUDIO = ROOT / "audio"
VIDEO = ROOT / "video"


def texts():
    return list(TEXT.rglob("*"))


def images():
    return list(IMAGE.rglob("*"))


def audios():
    return list(AUDIO.rglob("*"))


def videos():
    return list(VIDEO.rglob("*"))
