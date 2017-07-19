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
        self.intro = "JSON Graph REPL v.{}".format(VERSION)


    def _load_graph(self):
        ''' Load the graph from a JSON file and pre-compute some helper 
        data structures for speedier access. '''
        self.poutput("*** Loading graph from '{}'...".format(self.filepath))
        with open(self.filepath) as json_file:
            self.graph = json.load(json_file)['graph']
        self._set_cwd('/')
        self._nodes = {}
        self._children = defaultdict(set)
        self._parents = defaultdict(set)
        for edge in self.graph['edges']:
            self._children[edge['source']].add(edge['target'])
            self._parents[edge['target']].add(edge['source'])
        for node in self.graph['nodes']:
            self._nodes[node['id']] = node
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


    def _current_node(self):
        return self._nodes[self._current_node_id()]

    def _set_cwd(self, cwd):
        self.cwd = cwd
        self.prompt = "{} >".format(self.cwd)


    def _parse_args(self, args_str):
        args = []
        opts = []
        for arg in args_str.split(' '):
            if arg.startswith('-'):
                arg = arg.strip('--').strip('-')
                opts.append(arg)
            else:
                args.append(arg)
        return args, opts


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
        args, opts = self._parse_args(args)
        for node_id in self._current_children():
            output_line = "{}".format(node_id)
            if 'l' in opts:
                node = self._nodes[node_id]
                output_line += "\t{}\t{}".format(node['type'], node['label'])
            self.poutput(output_line)

    def do_info(self, args):
        args, opts = self._parse_args(args)
        if self.cwd == '/':
            self.poutput("CURRENT GRAPH: {} ('{}')".format(self.graph.get('label', ''), self.filepath))
            self.poutput("GRAPH TYPE: {}".format(self.graph.get('type')))
            self.poutput("NODES: {}".format(len(self.graph['nodes'])))
            self.poutput("EDGES: {}".format(len(self.graph['edges'])))
            self.poutput("META: {}".format(self.graph.get('metadata', {})))
        else:
            node = self._current_node()
            self.poutput("NODE ID: {}".format(node['id']))
            self.poutput("NODE TYPE: {}".format(node['type']))
            self.poutput("NODE LABEL: {}".format(node.get('label', '')))
            self.poutput("META: {}".format(node.get('metadata', {})))
