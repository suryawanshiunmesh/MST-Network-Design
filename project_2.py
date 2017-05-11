# Unmesh Suryawanshi
# qd6395
# CS 6591: CNAD - Project 2

# Libraries
from math import *
from collections import deque

# Declaration of Variables
traffic = 0
graph = []
mst = []
node = []
node_loc = 0
edge_wt = x = [[0 for i in range(10)] for j in range(10)]
traffic_table = [[0 for i in range(10)] for j in range(10)]
mst_matrix = [[0 for i in range(11)] for j in range(11)]
load = [[0 for i in range(11)] for j in range(11)]

# Input Files
node_loc_file = "n.txt"
traffic_table_file = "t.txt"

# Fetching the value from node loc file
def read_node_loc(fnode_loc):
    global node_loc
    with open(fnode_loc) as f:
        node_loc = [[int(x) for x in line.split()] for line in f]


# Function for calculating Weight of edges
def calc_edge_weight():
    global edge_wt
    for i in xrange(10):
        for j in xrange(10):
            temp = (node_loc[i][1] - node_loc[j][1]) *(node_loc[i][1] - node_loc[j][1]) + (node_loc[i][2] - node_loc[j][2]) *(node_loc[i][2] - node_loc[j][2])
            edge_wt[i][j] = sqrt(temp)



def fun1():
    global graph
    for i in xrange(10):
        for j in xrange(i+1, 10):
            temp = (i+1, j+1)
            graph.append([edge_wt[i][j], temp])



def search_value(ele):
    global node
    if ele != node[ele]:
        node[ele] = search_value(node[ele])
    return node[ele]


# fun1ion of kruskal algorithm
def kruskal():
    global graph, node, mst_matrix, mst_weight
    graph.sort(key=lambda x: x[0])
    mst_weight = 0
    for i in xrange(11):
        node.insert(i,i)
# Displaying MST
    print 'MST: '
    for i in xrange(len(graph)):
        nn1 = graph[i][1][0]
        nn2 = graph[i][1][1]
        set1 = search_value(nn1)
        set2 = search_value(nn2)
        if set1 != set2:
            mst.append(graph[i])
            mst_matrix[nn1][nn2] = 1
            mst_matrix[nn2][nn1] = 1
            node[set1] = node[set2]
            mst_weight = mst_weight + graph[i][0]
            print nn1, ' ', nn2, ' ', graph[i][0], ' Km'
    print 'MST Weight =', mst_weight, 'Km'


# Fetching values from traffic table
def read_traffic_table(ftraffic_table):
    global traffic_table, traffic
    with open(ftraffic_table) as f:
        traffic = [[int(x) for x in line.split()] for line in f]
    for n1, n2, load in traffic:
        traffic_table[n1 - 1][n2 - 1] = load

# Implemenation of searching algo : Breadth search algorithm
def breadth_first_search(src, dest, path_load):
    global mst_matrix, load
    k = [0 for j in range(11)]
    main_dict = {}
    main_dict[src] = 0
    q = []
    q.append(src)
    k[src] = 1
    found = False
    while(len(q) != 0):
        nn1 = q.pop()

        for nn2 in xrange(1, 11):
            if mst_matrix[nn1][nn2] == 0:
                continue
            if k[nn2] == 0:
                main_dict[nn2] = nn1
                q.append(nn2)
                if nn2 == dest:
                    break
        k[nn1] = 2
        if found is True:
            break

    now = dest
    path_length = 0

    while(main_dict[now] != 0):
        load[main_dict[now]][now] = load[main_dict[now]][now] + path_load
        now = main_dict[now]
        path_length = path_length + 1

    return path_length - 1

# Calculating load
def calc_load():
    global traffic, mst, load
    for i in xrange(len(traffic)):
        path_length = breadth_first_search(traffic[i][0],
                                           traffic[i][1],
                                           traffic[i][2])
        traffic[i].append(path_length)

# Set value
    max_link_load = 0
    avg_link_load = 0
    link_count = 0

# Displaying Utilization of each link
    print '\nUtilization of Links: '
    for i in xrange(len(mst)):
        nn1 = mst[i][1][0]
        nn2 = mst[i][1][1]
        link_load = load[nn1][nn2] + load[nn2][nn1]
        print nn1, ' ', nn2, ' ', link_load, ' Kbps', link_load*100/float(1544), '%'
        if link_load > max_link_load:
            max_link_load = link_load
        avg_link_load = avg_link_load + link_load
        link_count = link_count + 1

# Displaying values of max Utilization and average Utilization
    print 'Max Utilization     =', float(max_link_load)*100/1544, '%'
    print 'Average Utilization =', float(avg_link_load)*100/(1544*link_count), '%'
    print '\nPath Lengths: '

    a = b = 0
    for i in xrange(len(traffic)):
        print traffic[i][0], ' ', traffic[i][1], ' ',traffic[i][2], 'Kbps', traffic[i][3] + 1, ' hops'
        a = a + traffic[i][2] * traffic[i][3]
        b = b + traffic[i][2]

# Displaying the values of Average hopes and average delays
    avg_hops = (float(a) / float(b)) + 1
    print 'Average Hops =', avg_hops, 'Hops'
    temp2  = float(max_link_load)/1544
    temp3 = float(1024*8)/(1544*1000)
    avg_delay = float(temp3 * avg_hops) / (1 - temp2)
    print '\n3 factors of average delay and the average delay:'
    print 'TBar            = ', temp3, 'sec'
    print 'Average Hops    =', avg_hops, 'Hops'
    print 'Max Utilization =', float(max_link_load)*100/1544, '%'
    print "\nAverage Delay   =", avg_delay, 'Sec'

# Main Function
if __name__ == '__main__':
    read_node_loc(node_loc_file)
    calc_edge_weight()
    fun1()
    kruskal()
    read_traffic_table(traffic_table_file)
    calc_load()
