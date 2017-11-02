#!/usr/bin/env python3
from app.configure_process import processor

if __name__ == "__main__":
    import getopt
    import sys

    opts, args = getopt.getopt(sys.argv[1:], '-h-f:-v', ['help', 'filename=', 'version'])
    # for opt_name, opt_value in opts:
    #     if opt_name in ('-h', '--help'):
    #         print("[*] Help info")
    #         exit()
    if len(args) != 0:
        processor(args[0])
    else:
        print("param can't be None")
        exit()
