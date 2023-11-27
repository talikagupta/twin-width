import sys
from queue import PriorityQueue
from cmath import inf

# 2 min black degree vertices
# 2 min red degree vertices approach
def max_rd(g):
    (black_edges, red_edges)= g
    # find the node with the max red degree
    maxr = -float('inf')
    x = None
    for i in red_edges:
        if(len(red_edges[i]) > maxr and len(red_edges[i])!=0):
            x = i
            maxr = len(red_edges[i])
    print(x, maxr)
    if x == None:
        # otherwise, find the node with the least black deg
        maxr = float('inf')
        for i in black_edges:
            if(len(black_edges[i]) < maxr):
                x = i
                maxr = len(black_edges[i])

    min_diff = float('inf')
    z = black_edges[x].union(red_edges[x])
    y = None
    for v in z:
        initial_red_edges = len(red_edges[v].union(red_edges[x]))
        final_red_edges =  calculate_rd(g, x, v)
        difference = final_red_edges - initial_red_edges # we want this to be as -ve as possible
        if(difference < min_diff):
            y = v
            min_diff = difference
    print(min_diff)
    pair = None
    if(x < y):
        pair = (y, x)
    else:
        pair = (x, y)
    return (x, y)




# calculate red degree after contracting x & y
def calculate_rd(g, x, y):
    (black_edges, red_edges) = g
    a = black_edges[x].symmetric_difference(black_edges[y])
    b = red_edges[x].union(red_edges[y])
    z = a.union(b)
    z.discard(x)
    z.discard(y)
    return len(z)

# Read the graph from a file
def parse(file):
    #file = open(file)

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

    black_edges.pop(w)
    red_edges.pop(w)

    # for x in black_edges[v]:
    #     z = len(black_edges[x])
    #     bd_pq.put((z, x))
    # bd_pq.put((len(black_edges[v]), v))
    # for x in to_check:
    #     z = len(red_edges[x])
    #     rd_pq.put((z, x))
    # rd_pq.put((len(red_edges[v]), v))

    
def add_edge(g,e):
    (v,w) = e
    if v != w:
        g[v].add(w)
        g[w].add(v)
               
def remove_edge(g,e):
    (v,w) = e
    g[v].discard(w)
    g[w].discard(v)

#path = 'tiny010.gr'
# path = 'heuristic-public/heuristic_018.gr'


# def initialization(g):
#     (black_edges, red_edges) = g
#     q1 = PriorityQueue()
#     for x in black_edges:
#         q1.put((len(black_edges[x]), x))

#     q2 = PriorityQueue() # initially empty
#     return q1, q2


if __name__ == '__main__':

    if len(sys.argv) > 1 and len(sys.argv[1].strip()) > 0:
        with open(str(sys.argv[1])) as inp:
            g = parse(inp)
    else:
        g = parse(sys.stdin)
#bd_pq, rd_pq = initialization(g) # black degree pq, red degree pq

# you either choose 2 min black degree vertices or 2 min red degree vertices -- whichever one gives the least rd after contraction
# how do you update the pq's? -- inside the contract

# def contract_next(g):
#     (black_edges, red_edges) = g
#     x_b = None
#     bd1 = None
    
#     while(bd_pq.empty() == False):

#         bd, z = bd_pq.get()
        
#         if(z in black_edges and bd == len(black_edges[z])):
#             x_b = z
#             bd1 = bd
#             break
    
#     y_b = None
#     bd2 = None
#     while(bd_pq.empty() == False):

#         bd, z = bd_pq.get()
#         if(z in black_edges and bd == len(black_edges[z]) and z!=x_b):
#             y_b = z
#             bd2 = bd
#             break
    
#     x_r, y_r = None, None
#     rd1, rd2 = None, None
    
#     while(rd_pq.empty() == False):

#         rd, z = rd_pq.get()
#         if(z in red_edges and rd == len(red_edges[z]) and z!=x_b and z!=y_b):
#             x_r = z
#             rd1 = rd
#             break
    
#     while(rd_pq.empty() == False):
#         rd, z = rd_pq.get()
#         if(z in red_edges and rd == len(red_edges[z]) and z!=x_b and z!=y_b and z!=x_r):
#             y_r = z
#             rd2 = rd
#             break
    
#     vertex_list = [x_b, y_b, x_r, y_r]
#     rd_list = [bd1, bd2, rd1, rd2]
#     min_rd = float('inf')
    
#     xf, yf = None, None
#     i1, i2 = None, None
#     for i, x in enumerate(vertex_list):
#         for j, y in enumerate(vertex_list):
#             if(x == None or y == None): continue
#             if(x <= y): continue
#             rd = calculate_rd(g, x, y)
#             if(rd < min_rd):
#                 xf, yf, i1, i2, min_rd = x, y, i, j, rd
#     for i in range(0, len(vertex_list)):
#         if(i != i1 and i != i2):
#             if(i < 2 and vertex_list[i]!=None):
#                 bd_pq.put((rd_list[i], vertex_list[i]))
#             elif(i>=2 and vertex_list[i]!=None):
#                 rd_pq.put((rd_list[i], vertex_list[i]))
                
#     return (xf, yf)
    

def form_cs(g):
    
    cs = []
    
    while(len(g[0]) != 1):
        (x, y) = max_rd(g)
        print(x, y)
        
        cs.append([x, y])
        rd = contract(g,(x,y))
        
       

    return cs


contraction_seq = form_cs(g)

res_file  = open('result1.tww', 'w')
for c in contraction_seq:
    res_file.write(f'{c[0]} {c[1]}')
    res_file.write('\n')
res_file.close()