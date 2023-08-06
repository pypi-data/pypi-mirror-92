__version__ = '0.1'

from time import sleep

from pyautogui import typewrite
from pyperclip import paste
from typer import run


def main(wait: int = 2):
    sleep(wait)
    typewrite(paste())


if __name__ == '__main__':
    run(main)
