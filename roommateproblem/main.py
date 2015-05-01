from itertools import repeat
import networkx as nx
import copy, sys, csv

csv_f = csv.reader(open('matchingdata.csv'))
n = int(csv_f.next()[0])

students = []

# maps students to their list of answers
scores = {}

def calculateScore(l1, l2):
    score = 0
    n = len(l1)
    for i in xrange(0, n):
        score += n - abs(int(l1[i]) - int(l2[i]))
    return score

# represent the problem as an undirected graph
G = nx.XGraph()

# fill in scores dictionary
for i in xrange(0, n):
    s1 = csv_f.next()[0]
    s2 = csv_f.next()[0]
    spl = s2.split(' ')
    students.append(s1)
    scores[s1] = spl

# add compability score edges to the graph
for i in xrange(0, n):
    for j in xrange(i, n):
        score = calculateScore(scores[students[i]], scores[students[j]])
        G.add_edge(students[i],students[j],score)

# vertex list
gnodes = G.nodes()

# None for no label
# 1 for S-blossom
# 2 for T-blossom
label = {}

# edge through which blossom attained its label
labeledge = {}

# every vertex is first its own root
root = {}

# immediate parent of a sub-blossom, otherwise None if already a top-level blossom
parents = {}

# base vertex of a sub-blossom
bases = {}

# least slack edge to a different S-vertex or blossom
bestedge = {}

# vertex's corresponding variable in the dual program
vdual = {}

# blossom's corresponding variable in the dual program
bdual = {}

# edges with zero slack
allowedge = {}

# queue of newly discovered S-vertices.
queue = []

# maximum edge weight.
maxweight = 0

# dictionary to be returned
roommates = {}

for k in G.edges_iter():
    (_, _, weight) = k
    if weight > maxweight:
        maxweight = weight

for v in gnodes:
    root[v] = v
    parents[v] = None
    bases[v] = v
    vdual[v] = maxweight

# dummy node
class Dummy:
    pass

class Blossom:
    # subblossoms: list of subblossoms
    # edges: list of connecting edges
    # leastslackedges: list of least slack edges to S-blossom neighbors
    __slots__ = ['subblossoms', 'edges', 'leastslackedges']

    def leaves(self):
        for t in self.subblossoms:
            if isinstance(t, Blossom):
                for v in t.leaves():
                    yield v
            else:
                yield t

# replace with proper directories as necessary
execfile("/Users/johngee/Documents/testing/slack.py")
execfile("/Users/johngee/Documents/testing/assignlabel.py")
execfile("/Users/johngee/Documents/testing/constructblossom.py")
execfile("/Users/johngee/Documents/testing/liftblossom.py")
execfile("/Users/johngee/Documents/testing/augmentblossom.py")
execfile("/Users/johngee/Documents/testing/augmentmatching.py")
execfile("/Users/johngee/Documents/testing/findaugmentingpath2.py")
execfile("/Users/johngee/Documents/testing/findaugmentingpath.py")
execfile("/Users/johngee/Documents/testing/findmaximummatching.py")

find_maximum_matching()
for key in sorted(roommates.keys()):
    print key + " gets matched with " + roommates[key]