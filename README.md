# json-graph-repl
Extensible command-line REPL for interacting with JSON graphs containing business objects. 

The JSON format is based on the `json-graph` specification at: https://github.com/jsongraph/json-graph-specification 

Sample graphs are provided in the `tests` directory. 

To use from the command line, just point the `jgrepl` tool to your JSON graph:

    $ ./jgrepl/jgrepl.py tests/food-graph.json 

Once in the REPL, type `help` for the list of available commands. Use `ctrl-d` to exit. 
