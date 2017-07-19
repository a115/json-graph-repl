import json

from cmd2 import Cmd

class App(Cmd):
    def __init__(self, filepath):
        self.intro = "JSON Graph REPL"
        self.allow_cli_args = False
        Cmd.__init__(self, use_ipython=True)
        self.filepath = filepath
        with open(filepath) as json_file:
            self.graph = json.load(json_file)
