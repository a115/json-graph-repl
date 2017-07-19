import json

from cmd2 import Cmd

import graph_utils as gu

class App(Cmd):
    def __init__(self, filepath):
        self.intro = "JSON Graph REPL"
        self.allow_cli_args = False
        Cmd.__init__(self, use_ipython=True)
        self.filepath = filepath
        with open(filepath) as json_file:
            self.graph = json.load(json_file)['graph']
        self.cwd = '/'
        self.root_nodes = gu.get_root_nodes(self.graph)

    def do_pwd(self, _args):
        self.stdout.write(self.cwd + '\n')

    def do_ls(self, args):
        for root_node in self.root_nodes:
            self.stdout.write(root_node + '\n')
