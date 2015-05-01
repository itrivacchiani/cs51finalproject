from itertools import repeat
import copy, sys, csv, os

data = open('matchingdata.csv')
csv_f = csv.reader(data)
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

execfile("roommateproblem/graph.py")

# represent the problem as an undirected graph
G = Graph()

# fill in scores dictionary
for i in xrange(0, n):
    s1 = csv_f.next()[0]
    s2 = csv_f.next()[0]
    spl = s2.split(' ')
    students.append(s1)
    scores[s1] = spl

# add compability score edges to the graph
for i in xrange(0, n):
    for j in xrange(i + 1, n):
        score = calculateScore(scores[students[i]], scores[students[j]])
        G.add_edge(students[i],students[j],score)

# None for no label
# 1 for S-blossom
# 2 for T-blossom
lbl = {}

# edge through which blossom attained its label
elbl = {}

# every vertex is first its own root
root = {}

# immediate parent of a sub-blossom, otherwise None if already a top-level blossom
parents = {}

# base vertex of a sub-blossom
bases = {}

# least slack edge to a different S-vertex or blossom
leastslack = {}

# vertex's corresponding variable in the dual program
vdual = {}

# blossom's corresponding variable in the dual program
bdual = {}

# edges with zero slack
zeroslack = {}

# queue of newly discovered S-vertices.
Svertexqueue = []

# maximum edge weight.
maxweight = 0

# dictionary to be returned
roommates = {}

for k in G.edges:
    (_, _, weight) = k
    if weight > maxweight:
        maxweight = weight

for v in G.nodes:
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

    def lvertices(self):
        for t in self.subblossoms:
            if isinstance(t, Blossom):
                for v in t.lvertices():
                    yield v
            else:
                yield t

# replace with proper directories as necessary
execfile("roommateproblem/edgeslack.py")
execfile("roommateproblem/assignlabel.py")
execfile("roommateproblem/constructblossom.py")
execfile("roommateproblem/liftblossom.py")
execfile("roommateproblem/augmentblossom.py")
execfile("roommateproblem/augmentmatching.py")
execfile("roommateproblem/findaugmentingpath2.py")
execfile("roommateproblem/findaugmentingpath.py")
execfile("roommateproblem/findmaximummatching.py")

find_maximum_matching()

print "\nAssignment:"
for key in sorted(roommates.keys()):
    print key + " <--> " + roommates[key]

data.close()
os.system("python menu.py")