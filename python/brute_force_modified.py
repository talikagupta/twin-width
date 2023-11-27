from cmath import inf
import copy
import itertools
from graph_networkx import Graph
import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue


def initialization(graph):
    
    q = PriorityQueue()
    
    for x in graph.g.nodes:
        for y in graph.g.nodes:
            if x == y: continue
            # calculate the red degree after contracting the pair
            temp_g = copy.deepcopy(graph)
            temp_g.contract(x, y)
            max_red_degree = temp_g.max_red_degree()
            q.put((max_red_degree,[x, y]) )
    
    return q


def find_contraction_sequence(q, graph):
  contraction_sequence = []

  # somewhere we need to keep track of the twin width up till each contraction step 
  final_tww = -1
  # continue contracting vertices until only one vertex is left in the graph
  while graph.g.number_of_nodes() > 1:
    red_degree, nodes_list = q.get()
    #print(red_degree)
    if red_degree > final_tww:
        final_tww = red_degree
    x = nodes_list[0]
    y = nodes_list[1]
    next_x, next_y = x, y
    
    nbr_x = list(graph.g.neighbors(x)) + [x]
    nbr_y = list(graph.g.neighbors(y))
    graph.contract(next_x, next_y)
    contraction_sequence.append([next_x, next_y])
    # updation of the pq
    temp_queue = PriorityQueue()
    
    temp_queue.queue = copy.deepcopy(q.queue)
    for item in q.queue:
        x_i = item[1][0]
        y_i = item[1][1]
        if ( x_i == y or y_i == y):
            temp_queue.queue.remove(item)
            continue
        if(x_i in nbr_x or x_i in nbr_y or y_i in nbr_x or y_i in nbr_y):
            temp_g = copy.deepcopy(graph)
            temp_g.contract(x_i, y_i)
            temp_queue.queue.remove(item)
            red_degree_i = temp_g.max_red_degree()
            temp_queue.put((red_degree_i, [x_i, y_i]))
    q = PriorityQueue()
    q.queue = copy.deepcopy(temp_queue.queue)
  
  return final_tww, contraction_sequence




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

k = 3

def find_contraction_sequence_recursive(graph, contraction_sequence):
    
    if len(contraction_sequence) == k:
        print(contraction_sequence)
        # temp graph can have red edges at the starting
        q = initialization(graph)
        tww, contraction_seq_greedy = find_contraction_sequence(q, graph)
        return tww, contraction_seq_greedy
    
    min_tw = float('inf')
    x_list = graph.g.nodes
    y_list = graph.g.nodes
    
    for x in x_list:
        for y in y_list:
            
            if x == y: continue
            
            contraction_sequence_i = contraction_sequence.copy()
            temp_graph = copy.deepcopy(graph)
            temp_graph.contract(x, y)
            contraction_sequence_i.append([x, y])
            final_tww, final_contraction_sequence = find_contraction_sequence_recursive(temp_graph, contraction_sequence_i)
            if(final_tww < min_tw):
                optimal_cs = final_contraction_sequence
                min_tw = final_tww
            
    return min_tw, optimal_cs

twin_width, contraction_seq = find_contraction_sequence_recursive(graph, [])

res_file  = open('./result1.tww', 'w')
for c in contraction_seq:
    res_file.write(f'{c[0]} {c[1]}')
    res_file.write('\n')
res_file.close()