# python module
from typing import List
from datetime import datetime


def add_space(strList: List[str]):
    if len(strList) > 0 and strList[-1] != "":
        strList.append("")


def get_name(name: str):
    if name is None:
        return "source"
    return name


def in_notebook() -> bool:
    # From: https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    # Tested in Jupyter, Hex, DeepNote and Colab
    try:
        import IPython

        return (
            hasattr(IPython.get_ipython(), "config")
            and len(IPython.get_ipython().config) > 0
        )
    except (NameError, ModuleNotFoundError):
        return False


def get_difference(time):
    return (time - datetime.now()).seconds


def get_datetime():
    return datetime.now().strftime("%Y-%m-%d$%H:%M")
