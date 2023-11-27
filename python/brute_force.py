from cmath import inf
import copy
import itertools
from graph_networkx import Graph
import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue

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
path = './tiny005.gr'

with open(path) as inp:
    graph = parse(inp)

def find_contraction_sequence_recursive(graph, contraction_sequence, twin_width):
    
    if graph.g.number_of_nodes() == 1:
        print(twin_width, " ", contraction_sequence)
        return twin_width, contraction_sequence
    
    x_list = graph.g.nodes
    y_list = graph.g.nodes
    min_tw = float('inf')
    optimal_cs = None
    #twin_width = graph.max_red_degree()
    
    for x in x_list:
        for y in y_list:
            if x == y: continue
            pass_twin_width = twin_width
            contraction_sequence_i = contraction_sequence.copy()
            temp_graph = copy.deepcopy(graph)
            temp_graph.contract(x, y)
            contraction_sequence_i.append([x, y])
            new_tw = temp_graph.max_red_degree()
            if new_tw > twin_width:
                pass_twin_width = new_tw
            final_twin_width, final_contraction_sequence = find_contraction_sequence_recursive(temp_graph, contraction_sequence_i, pass_twin_width)
            if(final_twin_width < min_tw):
                optimal_cs = final_contraction_sequence
                min_tw = final_twin_width
            
    return min_tw, optimal_cs

twin_width, contraction_seq = find_contraction_sequence_recursive(graph, [], 0)

res_file  = open('./result1.tww', 'w')
for c in contraction_seq:
    res_file.write(f'{c[0]} {c[1]}')
    res_file.write('\n')
res_file.close()