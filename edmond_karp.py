import csv, os

# bfs used in Edmonds-Karp
# this version returns a single valid path from source to sink
def bfs(G, F, source, sink):
	queue = [source]
	paths = {source: []}
	while queue:
		u = queue.pop(0)
		for v in G[u].keys():
			if G[u][v][0] - F[u][v][0] > 0 and v not in paths:
				paths[v] = paths[u] + [(u,v)]
				if v == sink:
					return paths[v]
				queue.append(v)
	return None

# Edmonds-Karp for max cardinality bipartite matching
# Input graph for max cardinality bipartite matching has source connected
# to all elements in set X, and all elements of set Y connected to sink.
# All edges have capacity = 1 (for max cardinality)
# The output is a triple (M,A,B) where M is a dictionary mapping
# members of V to their matches in U, A is the part of the maximum
# matching in U, and B is the part of the MIS in V
def edmonds_karp(G, source, sink):
	n = len(G) # C is the capacity matrix
	F = [[(0,0)] * n for i in xrange(n)]
	# residual capacity from u to v is C[u][v] - F[u][v]

	# keep augmenting paths from source until there is no path from it to sink
	while True:
		path = bfs(G, F, source, sink)
		if not path:
			break
		# traverse path to find smallest capacity
		flow = min(G[u][v][0] - F[u][v][0] for u,v in path)
		# traverse path to update flow
		for u,v in path:
			F[u][v] = (F[u][v][0] + flow, G[u][v][1])
			F[v][u] = (F[v][u][0] - flow, -G[u][v][1])

	maxflow = sum(F[source][i][0] for i in xrange(n))
	maxcap = sum(G[source][i][0] for i in G[source].keys())

	# find pairings
	matching = {}
	for u in xrange(n):
		if F[source][u][0] > 0:
			for v in xrange(n):
				if F[u][v][0] > 0:
					matching[v] = u
					break
	return (F, maxflow, matching)


#######################################################
# I/O
csv_f = csv.reader(open('graph.csv'))

problem = csv_f.next()[0].lower()
# csv file does not correctly indicate stable marriage or 
# hospital resident as the problem to be solved
if problem != "flow graph":
	print "The problem indicated in graph.csv is not max flow\n"
	print "Exiting to menu."
	os.system("python menu.py")

numVertices = int(csv_f.next()[0])
# initialize graph
graph = [{} for i in xrange(numVertices)]
vertexnames = csv_f.next()[0].split(' ')

# sink
for i in xrange(numVertices-1):
	vertexname = csv_f.next()[0]
	vertexindex = vertexnames.index(vertexname)
	s1 = csv_f.next()[0]
	s2 = csv_f.next()[0]
	s3 = csv_f.next()[0]
	neighborindices = [vertexnames.index(elt) for elt in s1.split(' ')]
	neighborcaps = [int(elt) for elt in s2.split(' ')]
	neighborcosts = [int(elt) for elt in s3.split(' ')]
	for v in xrange(len(neighborindices)):
		graph[vertexindex][neighborindices[v]] = (neighborcaps[v], neighborcosts[v])

# assume source and sink already added, last two vertices
source = numVertices - 2
sink = source + 1

F, maxflow, matching = edmonds_karp(graph, source, sink)

print "\nSolution:"
print "flow = %i" % maxflow
print "Matching:"
for a in matching.keys():
	print "%s <--> %s" % (vertexnames[a], vertexnames[matching[a]])

os.system("python menu.py")