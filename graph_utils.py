
def get_root_nodes(graph):
    all_children = set(e['target'] for e in graph['edges'])
    return [n['id'] for n in graph['nodes'] 
            if n['id'] not in all_children]
