conversions = []

#%% NexworkX graph

try:
    import networkx as nx
    nx_type = nx.classes.graph.Graph
    nx_di_type = nx.classes.digraph.DiGraph

    def nx_to(G):
        string = ""
        for line in nx.generate_graphml(G):
            string += line + "\n"
        return string

    def nx_from(string):
        return nx.parse_graphml(string)

    conversions.append((nx_type, nx_to, nx_from))
    conversions.append((nx_di_type, nx_to, nx_from))
except:
    pass

#%% List

def list_to(l):
    d = {}
    for i in range(len(l)):
        d[str(i)] = l[i]
    return d

def list_from(d):
    l = []
    for i in range(len(d)):
        l.append(d[str(i)])
    return l

conversions.append((list, list_to, list_from))
#%% Tuple

def tuple_to(t):
    return list_to(t)

def tuple_from(d):
    return tuple(list_from(d))

conversions.append((tuple, tuple_to, tuple_from))
#%% Nonetype

def none_to(*_):
    return "None"

def none_from(*_):
    return None

conversions.append([type(None), none_to, none_from])
#%%
from datetime import datetime

def date_to(d):
    return datetime.timestamp(d)

def date_from(ts):
    return datetime.fromtimestamp(ts)

conversions.append((datetime, date_to, date_from))