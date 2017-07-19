#!/usr/bin/env python

import argparse

from repl import App

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path to a JSON graph to load")
    args = parser.parse_args()

    app = App(filepath=args.filepath)
    app.cmdloop()
