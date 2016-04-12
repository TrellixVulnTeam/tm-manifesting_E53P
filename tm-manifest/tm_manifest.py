#!/usr/bin/python3 -tt
import argparse
from pdb import set_trace
import sys

from tmcmd import cmdlookup


def main(args):
    if len(sys.argv) < 2:
        cmdlookup['help']()
        return
    try:
        print(cmdlookup[sys.argv[1]](sys.argv[2:], **args))
    except Exception as e:
        print(str(e))
        if args['debug']:
            set_trace()
            pass


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(description='Optional arguments for API.')

    PARSER.add_argument('--verbose',
                        help='Make it talk.',
                        action='store_true')
    PARSER.add_argument('--debug',
                        help='Turn on debugging tool.',
                        action='store_true')
    ARGS, _ = PARSER.parse_known_args()
    main(vars(ARGS))

    raise SystemExit(0)
