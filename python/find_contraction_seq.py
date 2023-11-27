from cmath import inf
import copy
import itertools
from graph_networkx_old_2 import Graph
import networkx as nx
import matplotlib.pyplot as plt


# find the next pair of vertices to contract
def find_next_pair(graph):
    min_red_degree = float(inf)
    min_pair = None

    # iterate over all pairs of vertices
    
    for x in graph.g.nodes:
        for y in graph.g.nodes:
            if x == y: continue
            temp_g = copy.deepcopy(graph)

            temp_g.contract(x, y)

            max_red_degree = temp_g.max_red_degree()
            if max_red_degree < min_red_degree:
                min_red_degree = max_red_degree
                min_pair = (x, y)
    
    return min_red_degree, min_pair





def find_contraction_sequence(graph):
  contraction_sequence = []

  # continue contracting vertices until only one vertex is left in the graph
  while graph.g.number_of_nodes() > 1:
    #print(list(graph.g.nodes))
    # plt.figure(num=None, figsize=(10, 10), dpi=40)
    # nx.draw(graph.g, pos=nx.spectral_layout(graph.g))
    # plt.show()
    #exit(0)
    
    min_red_degree, (next_x, next_y) = find_next_pair(graph)
    print(min_red_degree, next_x, next_y)
    graph.contract(next_x, next_y)
    contraction_sequence.append([next_x, next_y])
    
  return contraction_sequence


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
            #for i in range(int(n)):
             #   g.add_node(i+1)
        else:
            graph.add_black_edge(int(li[0]), int(li[1]))
    return graph # graph obj


path = 'tiny005.gr'

with open(path) as inp:
    graph = parse(inp)


contraction_seq = find_contraction_sequence(graph)

res_file  = open('result1.tww', 'w')
for c in contraction_seq:
    res_file.write(f'{c[0]} {c[1]}')
    res_file.write('\n')
res_file.close()