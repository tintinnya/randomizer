# Author: @tintinnya
# version: 1.0
#
# This python script only for phun, not for gambling purpose
# use python3 and curses
#
import signal
import sys
import argparse
import random
import curses
from curses.textpad import Textbox, rectangle
from os import path
import mmap

stdscr = curses.initscr()
curses.noecho()

num_rows, num_cols = stdscr.getmaxyx()

def sigint_handler(signal, frame):
    stdscr.addstr(10, 1, "[-] SIGINT received. Quitting...")
    stdscr.refresh()
    curses.echo()
    curses.endwin()
    sys.exit(0)

'''
Load content and put it as mmap
'''
def loadFromFile(filename):
    if not path.exists(filename) or not path.isfile(filename):
        msg = "[-] {0} is not exists or not a file. Quiting...".format(filename)
        stdscr.addstr(10, 1, msg)
        stdscr.refresh()
        curses.echo()
        curses.endwin()
        sys.exit(1)
    with open(filename, "r") as f:
        mm = mmap.mmap(f.fileno(),0, access=mmap.ACCESS_READ)
    f.close()
    names = []
    for line in iter(mm.readline,b""):
        names.append(line)
    return names

def argumentBuilder():
    parser = argparse.ArgumentParser(description='Random picker for a winner')
    parser.add_argument('-f','--filename', dest='filename',required=True,help='TXT file that contains name to be picked')
    args = parser.parse_args()
    return args.filename

def printCenter(atRow, str, mode):
    pos = int((num_cols - len(str))/2)
    clear = " " * (num_cols - 2)
    stdscr.addstr(atRow, 1, clear, mode)
    stdscr.addstr(atRow, pos, str, mode)


def main():
    filename = argumentBuilder()
    namelist = loadFromFile(filename)

    while (True):
        numEntry = len(namelist)
        s = "Randomizer {0}x{1} processing {2} entries. Press [CTRL + C] to quit.".format(num_rows, num_cols,numEntry)
        stdscr.addstr(0, 0, s)
        rectangle(stdscr, 1,0, 1+1+1, 1+num_cols-3+1)
        #stdscr.addstr(2, 13, "Start")
        printCenter(2, "Start", curses.A_NORMAL)
        stdscr.getkey()
        printCenter(5, "", curses.A_NORMAL)

        sr = random.SystemRandom()
        printCenter(2, "Randomizing...", curses.A_BLINK)
        stdscr.refresh()

        i = numEntry
        while (i > 0):
            x = sr.randint(1,len(namelist))-1
            name = namelist[x].rstrip().decode("utf-8")
            printCenter(6, name, curses.A_NORMAL)
            stdscr.refresh()
            if (i < 20):
                curses.napms((20-i)*20)
            else:
                curses.napms(20)
            i = i - 1
        namelist.pop(x)

        printCenter(5, "Congratulation!", curses.A_NORMAL)
        stdscr.refresh()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    curses.wrapper(main())
