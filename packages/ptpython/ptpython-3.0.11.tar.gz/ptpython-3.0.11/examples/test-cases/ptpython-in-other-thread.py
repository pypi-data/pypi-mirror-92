#!/usr/bin/env python
"""
"""
import threading

from ptpython.repl import embed


def in_thread():
    embed(globals(), locals(), vi_mode=False)


def main():
    th = threading.Thread(target=in_thread)
    th.start()
    th.join()


if __name__ == "__main__":
    main()
