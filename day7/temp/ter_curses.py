#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

from curses import wrapper

def main(stdscr):
    stdscr.clear()
    for i in range(0, 11):
        v = i - 10
        stdscr.addstr(i, 0, "10 divided by {} is {}".format(v, 10/v))
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)