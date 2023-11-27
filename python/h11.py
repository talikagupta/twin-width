import sys
from queue import PriorityQueue
from cmath import inf

# find the min red deg vertex and go through all the n other nodes to find the one that gives the least rd

def min_red_deg_vertex(g):
    (black_edges, red_edges) = g
    min_red_deg_v = None
    min_rd = float('inf')
    for x in red_edges:
        if (len(red_edges[x]) < min_rd and len(red_edges[x])!=0):
            min_rd = len(red_edges[x])
            min_red_deg_v = x
    if(min_red_deg_v == None):
        
        min_bd = float('inf')
        for x in black_edges:
            if (len(black_edges[x]) < min_bd):
                min_bd = len(black_edges[x])
                min_red_deg_v = x

    return min_red_deg_v

def min_red_deg_list(g):
    black_edges, red_edges = g
    q = PriorityQueue()
    for x in black_edges:
        q.put((len(black_edges[x]), x))


# calculate red degree after contracting x & y
def calculate_rd(g, x, y):
    (black_edges, red_edges) = g
    a = black_edges[x].copy()
    a2 = black_edges[y].copy()
    b = red_edges[x].copy()
    b2 = red_edges[y].copy()
    a3 = a.symmetric_difference(a2)
    b3 = b.union(b2)
    z = a3.union(b3)
    z.discard(x)
    z.discard(y)
    return len(z)

# Read the graph from a file
def parse(file):
    file = open(file)

    # find first non-comment line
    line   = find_next_line(file)
    params = line.split()
    if params[0] == "p":
        n = int(params[2])
        m = int(params[3])   
        
    # initialize all edges and fill them with empty sets
    black_edges = {}
    red_edges   = {}
    for i in range(1, n+1):
        black_edges[i] = set()
        red_edges[i]   = set()

    # read the initial black edges
    for line in file.readlines():
        if line[0] != "c":
            (v,w) = line.split()
            if(v!=w):
                black_edges[int(v)].add(int(w))
                black_edges[int(w)].add(int(v))
            #add_edge( g, (int(v), int(w)) , 1)
            
    return (black_edges, red_edges)

def find_next_line(f):
    line = f.readline()
    # we have reached the end of the file
    if not line:
        return line
    # comment lines start with c
    while(line[0] == "c"):
        line = f.readline()
    return line

def contract(g, e):

    # We need to consider several different situations regarding vertices z
    # and their relation to v and w
    (v,w) = e
    (black_edges, red_edges) = g
    remove_edge(g, e, 1)
    remove_edge(g,   e,0)
    to_check = [v]

    to_be_removed_black = []
    for zw in black_edges[w]:
        # If z is connected to w, but not to v, add a red edge
        if zw not in black_edges[v]:
            add_edge(g,(zw,v),0)
            to_check.append(zw)            
        # As w will be removed, delete the edge
        to_be_removed_black.append((w,zw))

    to_be_removed_red = []            
    for zw in red_edges[w]:
        # All red edges of w are transfered to v
        add_edge(g,(zw,v),0)
        to_check.append(zw)        
        # Red edges replace black edges
        remove_edge(g,(zw,v), 1)
        # As w will be removed, delete the edge
        to_be_removed_red.append((w,zw))

    for ze in to_be_removed_red:
        remove_edge(g,ze, 0)

    for zv in black_edges[v]:
        # If z is connected to v, but not to w, replace the black edge by an red edge
        if zv not in black_edges[w]:
            add_edge(g,(zv,v),0)
            to_check.append(zv)                    
            to_be_removed_black.append((zv,v))

    for ze in to_be_removed_black:
            remove_edge(g,ze, 1)

    black_edges.pop(w)
    red_edges.pop(w)

    
def add_edge(g,e,f):
    
    black_edges, red_edges = g
    (v,w) = e
    if(v!=w):
        if(f == 1):
            black_edges[v].add(w)
            black_edges[w].add(v)
        else:
            red_edges[v].add(w)
            red_edges[w].add(v)
               
def remove_edge(g,e,f):
    black_edges, red_edges = g
    (v,w) = e
    if(f == 1):
        black_edges[v].discard(w)
        black_edges[w].discard(v)
    else:
        red_edges[v].discard(w)
        red_edges[w].discard(v)


def initial_pair(g):
    
    (black_edges, red_edges) = g
    # min black degree vertex
    min_deg_vertex = None
    min_deg = float('inf')
    for i in black_edges:
        if(len(black_edges[i]) < min_deg):
            min_deg = len(black_edges[i])
            min_deg_vertex = i
    
    min_sym_diff = float('inf')
    second_vertex = -1
    for v in black_edges[min_deg_vertex]:
        z = black_edges[min_deg_vertex].symmetric_difference(black_edges[v])
        z.discard(min_deg_vertex)
        z.discard(v)
        if(len(z) < min_sym_diff):
            second_vertex = v
            min_sym_diff = len(z)
    
    return (min_deg_vertex, second_vertex)


def contracting_vertices(g):

    
    (black_edges, red_edges) = g
    
    x = min_red_deg_vertex(g)
    y = None
    min_rd = float('inf')

    # if x in red_edges:  
    #     for v in red_edges[x]:
    #         rd_i = calculate_rd(g, x, v)
    #         if(rd_i < min_rd):
    #             y = v
    #             min_rd = rd_i
 
    
    # for v in black_edges[x]:
    #     rd_i = calculate_rd(g, x, v)
    #     if(rd_i < min_rd):
    #         y = v
    #         min_rd = rd_i
    avg_deg = 0
    min_bd = float('inf')
    max_bd = -float('inf')
    min_rd2 = float('inf')
    max_rd = -float('inf')

    for i in black_edges:
            if(i == x):
                continue
            else:
               rd = calculate_rd(g, x, i)
               if(rd < min_rd):
                   min_rd = rd
                   y = i
            avg_deg+=(len(black_edges[i])+len(red_edges[i]))
            min_bd = min(min_bd, len(black_edges[i]))
            max_bd = max(max_bd, len(black_edges[i]))
            min_rd2 = min(min_rd2, len(red_edges[i]))
            max_rd = max(max_rd, len(red_edges[i]))

    # avg_deg /= len(black_edges)
    # print("deg of y:",len(black_edges[y]), len(red_edges[y])) 
    # print("deg of x:",len(black_edges[x]), len(red_edges[x]))   
    # if(x in black_edges[y] or x in red_edges[y]):
    #     print(f'x and y are connected')
    # print("len of intersectiion", len(black_edges[x].intersection(red_edges[x])))
    # print("avg_deg ", avg_deg)
    # print(f'minbd = {min_bd}, maxbd = {max_bd}, minrd = {min_rd2}, maxrd = {max_rd}')

    
    # if(y == None):
    #     min_rd = float('inf')
    #     for i in black_edges:
    #         if(i == x):
    #             continue
    #         else:
    #            rd = calculate_rd(g, x, i)
    #            if(rd < min_rd):
    #                min_rd = rd
    #                y = i
    
    pair = None
    
    if(x < y):
        pair = (x, y)
    else:
        pair = (y, x)
    return pair

def form_cs(g):
    
    cs = []

    (x, y) = initial_pair(g)
    cs.append([x, y])
    contract(g,(x,y))
    
    while(len(g[0]) != 1):
        (x, y) = contracting_vertices(g)
        print(x, y)
        cs.append([x, y])
        rd = contract(g,(x,y))
       

    return cs


# if __name__ == '__main__':

#     if len(sys.argv) > 1 and len(sys.argv[1].strip()) > 0:
#         with open(str(sys.argv[1])) as inp:
#             g = parse(inp)
#     else:
#         g = parse(sys.stdin)
path = 'heuristic-public/heuristic_002.gr'
g= parse(path)
contraction_seq = form_cs(g)
res_file  = open('result1.tww', 'w')
for c in contraction_seq:
    res_file.write(f'{c[0]} {c[1]}')
    res_file.write('\n')
res_file.close()

# for c in contraction_seq:
#     print(f'{c[0]} {c[1]}')