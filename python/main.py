import sys
from queue import PriorityQueue
from cmath import inf

updated_pairs = {}

# calculate red degree after contracting x & y
def calculate_rd(g, x, y):
    (black_edges, red_edges) = g
    rd = 0
    a = black_edges[x].symmetric_difference(black_edges[y])
    b = red_edges[x].union(red_edges[y])
    z = a.union(b)
    z.discard(x)
    z.discard(y)
    return len(z)

    

def initialization(g):
    
    q = PriorityQueue()
    (black_edges, red_edges) = g
    for x in black_edges:
        for y in black_edges:
            if(x <= y): continue
            a = black_edges[x].copy()
            b = black_edges[y].copy()
            a.discard(y)
            b.discard(x)
            
            
            non_common_nbr = len(a.symmetric_difference(b))
            q.put((non_common_nbr,(x, y)))
            print("in pq", x, y, non_common_nbr)

    return q


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
            add_edge( black_edges, (int(v), int(w)) )
            
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


# Return the maximum red degree of the graph
# checking the red degree of only the newly contracted vertex and it's neighbours(that are connected to it by a red edge)
def red_deg(g, v):
    (black_edges, red_edges) = g
    tmps = [v]
    tmp = len(red_edges[v])
    for w in red_edges[v]:
        tmp = max(tmp, len(red_edges[w]))
        tmps.append(w)
    return tmp



# Contracts the vertices in e in g and update the edges
def contract(g, e):

    # We need to consider several different situations regarding vertices z
    # and their relation to v and w
    (v,w) = e
    (black_edges, red_edges) = g
    remove_edge(black_edges, e)
    remove_edge(red_edges,   e)
    to_check = [v]

    to_be_removed_black = []
    for zw in black_edges[w]:
        # If z is connected to w, but not to v, add a red edge
        if zw not in black_edges[v]:
            add_edge(red_edges,(zw,v))
            to_check.append(zw)            
        # As w will be removed, delete the edge
        to_be_removed_black.append((w,zw))

    to_be_removed_red = []            
    for zw in red_edges[w]:
        # All red edges of w are transfered to v
        add_edge(red_edges,(zw,v))
        to_check.append(zw)        
        # Red edges replace black edges
        remove_edge(black_edges,(zw,v))
        # As w will be removed, delete the edge
        to_be_removed_red.append((w,zw))

    for ze in to_be_removed_red:
        remove_edge(red_edges,ze)

    for zv in black_edges[v]:
        # If z is connected to v, but not to w, replace the black edge by an red edge
        if zv not in black_edges[w]:
            add_edge(red_edges,(zv,v))
            to_check.append(zv)                    
            to_be_removed_black.append((zv,v))

    for ze in to_be_removed_black:
            remove_edge(black_edges,ze)

    # remove w
    black_edges.pop(w)
    red_edges.pop(w)

    
    # for x in to_check:
    #     for zw in to_check:
    #         if(x == zw):
    #             continue
    #         rd = calculate_rd(g, x, zw)
    #         pair = None
    #         if(x < zw):
    #             pair = (zw, x)
    #         else:
    #             pair = (x, zw)
    #         updated_pairs[pair] = rd
    #         q.put((rd, pair))
            
    



# Add an edge e to the graph g    
def add_edge(g,e):
    (v,w) = e
    if v != w:
        g[v].add(w)
        g[w].add(v)
        
# Remove an edge e grom the graph g (if it exists)        
def remove_edge(g,e):
    (v,w) = e
    g[v].discard(w)
    g[w].discard(v)

#returns vertex to be contracted next
# most common nbrs
def contracting_vertices(g):
    (black_edges, red_edges) = g
    pair = None
    while(True):
        rd, pair = q.get()
        (x, y) = pair
        if(x not in black_edges or y not in black_edges):
            continue
        # elif(pair in updated_pairs and rd < updated_pairs[pair]):
        #     continue
        else:
            break
            
    return pair



# Check whether a given contraction sequence seq is valid for g.
# The sequence is only invalid if a removed vertex gets contracted or the graph is not contracted completely. 
def form_cs(g):
    
    cs = []

    while(len(g[0]) != 1):
        (x, y) = contracting_vertices(g)
        print(x, y)
        black_edges, red_edges = g
        print("deg of y:",len(black_edges[y]), len(red_edges[y])) 
        print("deg of x:",len(black_edges[x]), len(red_edges[x]))   
        if(x in black_edges[y] or x in red_edges[y]):
            print(f'x and y are connected')
        cs.append([x, y])
        rd = contract(g,(x,y))
       

    return cs


#path = 'tiny010.gr'
path = 'heuristic-public/heuristic_002.gr'

#path_list = ['tiny001.gr', 'tiny002.gr', 'tiny003.gr', 'tiny004.gr', 'tiny005.gr', 'tiny006.gr', 
#'tiny007.gr', 'tiny008.gr', 'tiny009.gr', 'tiny010.gr']
#actual_tww = [1, 2, 0, 0, 3, 0, 2, 4, 1, 2]
#my_tww =     [1, 2, 0, 0, 4, 0, 2, 4, 1, 2] 1 mismatch
# new method = [1, 2, 0, 0, 4, 0, 2, 4,1,  2 ]

g = parse(path)
q = initialization(g)

contraction_seq = form_cs(g)

res_file  = open('result1.tww', 'w')
for c in contraction_seq:
    res_file.write(f'{c[0]} {c[1]}')
    res_file.write('\n')
res_file.close()

# if __name__ == '__main__':

#     if len(sys.argv) > 1 and len(sys.argv[1].strip()) > 0:
#         with open(str(sys.argv[1])) as inp:
#             g = parse(inp)
#         #g = parse(sys.argv[1])
#     else:
#         g = parse(sys.stdin)

# q = initialization(g)
# contraction_seq = form_cs(g)

# for c in contraction_seq:
#     print(f'{c[0]} {c[1]}')