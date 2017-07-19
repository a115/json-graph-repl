import os
import json
from collections import defaultdict

from cmd2 import Cmd

VERSION = '0.1'

class App(Cmd):

    def __init__(self, filepath):
        self.allow_cli_args = False
        Cmd.__init__(self, use_ipython=True)
        self.filepath = filepath
        self._load_graph()
        self.intro = "JSON Graph REPL v.{}. Working with: '{}'".format(
                VERSION, filepath)


    def _load_graph(self):
        ''' Load the graph from a JSON file and pre-compute some helper 
        data structures for speedier access. '''
        with open(self.filepath) as json_file:
            self.graph = json.load(json_file)['graph']
        self._set_cwd('/')
        self._children = defaultdict(set)
        self._parents = defaultdict(set)
        for edge in self.graph['edges']:
            self._children[edge['source']].add(edge['target'])
            self._parents[edge['target']].add(edge['source'])
        self.root_nodes = [n['id'] for n in self.graph['nodes'] 
                           if not self._parents[n['id']]]


    def _current_node_id(self):
        return self.cwd.split('/')[-1]


    def _children_for(self, node_id):
        if node_id:
            return self._children[node_id]
        return self.root_nodes


    def _current_children(self):
        return self._children_for(self._current_node_id())

    def _set_cwd(self, cwd):
        self.cwd = cwd
        self.prompt = "{} >".format(self.cwd)


    ################################
    # Generic command definitions:
    #

    def do_pwd(self, _args):
        self.poutput(self.cwd)


    def do_cd(self, args):
        if args.startswith('/'):
            self._set_cwd('/')
            args.strip('/')
 
        for component in args.split('/'):
            if not component:
                continue
            if component == '..':
                self._set_cwd(os.path.abspath(os.path.join(self.cwd, '..')))
            else:
                if component in self._current_children():
                    self._set_cwd(os.path.join(self.cwd, component))
                else:
                    self.perror("Node not found: '{}'\n".format(component))


    def do_ls(self, args):
        for node_id in self._current_children():
            self.poutput(node_id)
