from cmath import inf
import copy
import itertools

import numpy as np
from graph_networkx import Graph
import networkx as nx
import matplotlib.pyplot as plt

# python verifier.py tiny001.gr result1.tww 

def parse(path):
    
    graph = None
    n = 0
    m = 0
    for line in path:
        if line[0] == 'c':
            continue
        line = line.replace('\n', '')
        li = line.split(" ")
        
        if li[0] == 'p':
            n = li[2]
            m = li[3]
            graph = Graph(int(n))
        else:
            graph.add_black_edge(int(li[0]), int(li[1]))
    return graph # graph obj


# path to the graph
path = 'exact-public/exact_136.gr'
    
with open(path) as inp:
    graph = parse(inp)

edges = graph.g.edges()
colors = [graph.g[u][v]['color'] for u,v in edges]
#pos = nx.spring_layout(graph.g)
pos = nx.spring_layout(graph.g, k=2, iterations=1)

i = 1
#plt.title(f'Start')
plt.figure(figsize=(30,15))
nx.draw(graph.g, pos = pos, edge_color=colors,with_labels=True)


plt.savefig(f'gr05_optimal_viz/fig{i}.png')
plt.show()
i+=1


# optimal answer goes in the optimal_contraction_seq.txt file
# res_file  = open('result1.tww', 'r')
# for c in res_file:
#     l = c.split()
#     a = int(l[0])
#     b = int(l[1])
#     print(a, b)
#     graph.contract(a, b)
#     edges = graph.g.edges()
#     colors = [graph.g[u][v]['color'] for u,v in edges]
#     #pos = nx.spring_layout(graph.g)
#     plt.title(f'After contracting {a} - {b}')
#     nx.draw(graph.g, pos= pos, edge_color=colors, with_labels=True)
    
    
#     plt.savefig(f'gr05_optimal_viz/fig{i}.png')
#     plt.show()
#     i+=1
# res_file.close()
