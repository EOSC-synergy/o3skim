"""This module offers some utils for code management.
"""
from contextlib import contextmanager
import os


@contextmanager
def cd(dir):
    """Changes the directory inside a 'with' context. When the code
    reaches the end of the 'with' block or the code fails, the
    previous folder is restored.

    :param dir: Path folder where to change the working directory.
    :type dir: str
    """
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(dir))
    try:
        yield
    finally:
        os.chdir(prevdir)
