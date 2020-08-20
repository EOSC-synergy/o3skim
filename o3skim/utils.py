"""This module offers some utils for code management"""
from contextlib import contextmanager
import os


@contextmanager
def cd(newdir):
    """Changes the directory inside a 'with' context"""
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
