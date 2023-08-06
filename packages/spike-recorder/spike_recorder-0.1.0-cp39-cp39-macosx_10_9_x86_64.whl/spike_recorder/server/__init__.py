# -*- coding: utf-8 -*-
import os
import sys
from multiprocessing import Process, Queue

from ._core import __doc__, run

def run_wrapper():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run()


def launch(is_async: bool = False):
    p = Process(target=run_wrapper)
    p.start()

    if not is_async:
        p.join()

    return p

