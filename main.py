#!/usr/bin/env python3
import getopt
import sys

from app.configure_process import processor

if __name__ == "__main__":
    version = 0.1
    opts, args = getopt.getopt(sys.argv[1:], '-h-v', ['help', 'version'])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("Usage: python3 main.py [FILE]")
            exit()
        if opt_name in ('-v', '--version'):
            print(f'version {version}')
    if len(args) != 0:

        processor(args[0])
    else:
        print("param can't be None")
        exit()
