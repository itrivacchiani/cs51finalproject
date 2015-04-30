# bfs used in Edmonds-Karp
# this version returns a single valid path from source to sink
def bfs(G, F, source, sink):
	queue = [source]
	paths = {source: []}
	while queue:
		u = queue.pop(0)
		for v in G[u].keys():
			if G[u][v][0] - F[u][v] > 0 and v not in paths:
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
	F = [[0] * n for i in xrange(n)]
	# residual capacity from u to v is C[u][v] - F[u][v]

	# keep augmenting paths from source until there is no path from it to sink
	while True:
		path = bfs(G, F, source, sink)
		if not path:
			break
		# traverse path to find smallest capacity
		flow = min(G[u][v][0] - F[u][v] for u,v in path)
		# traverse path to update flow
		for u,v in path:
			F[u][v] += flow
			F[v][u] -= flow

	# find pairings
	matching = {}
	A = []
	B = []
	for u in F[source]:
		if F[source][u] > 0:
			A.append[u]
			for v in F[u]:
				if F[u][v] > 0:
					matching[v] = u
					B.append[v]
					break
	return (matching, A, B)

# Hopcroft-Karp for max cardinality bipartite matching
# The output is a triple (M,A,B) where M is a dictionary mapping
# members of V to their matches in U, A is the part of the maximum
# independent set in U, and B is the part of the MIS in V
def hopcroft_karp(graph):
	# source and sink nodes are irrelevant
	graphSize = len(graph - 2)

	# initialize greedy matching (redundant, but faster than full search)
	matching = {}
	for u in xrange(len(graphSize)):
		for v in graph[u].keys():
			if v not in matching:
				matching[v] = u
				break

	# try to correct the matching to have disjoint edges
	while True:
		# structure residual graph into layers
		# pred[u] gives the neighbor in the previous layer for u in U
		# preds[v] gives a list of neighbors in the previous layer for v in V
		# unmatched gives a list of unmatched vertices in final layer of V, and
		# is also used as a flag value for pred[u] when u is in the first layer
		preds = {}
		unmatched = []
		pred = dict([(u,unmatched) for u in xrange(graphSize)])
		for v in matching:
			del pred[matching[v]]
		layer = list(pred)

		# repeatedly extend layering structure by another pair of layers
		while layer and not unmatched:
			newLayer = {}
			for u in layer:
				for v in graph[u].keys():
					if v not in preds:
						newLayer.setdefault(v,[]).append(u)
			layer = []
			for v in newLayer:
				preds[v] = newLayer[v]
				if v in matching:
					layer.append(matching[v])
					pred[matching[v]] = v
				else:
					unmatched.append(v)

		# check if finished layering without finding any alternating paths
		if not unmatched:
			unlayered = {}
			for u in xrange(graphSize):
				for v in graph[u].keys():
					if v not in preds:
						unlayered[v] = None
			return (matching,list(pred),list(unlayered))

		# recursively search backward through layers to find alternating paths
		# recursion returns true if found path, false otherwise
		def recurse(v):
			if v in preds:
				L = preds[v]
				del preds[v]
				for u in L:
					if u in pred:
						pu = pred[u]
						del pred[u]
						if pu is unmatched or recurse(pu):
							matching[v] = u
							return 1
			return 0

		for v in unmatched: recurse(v)

# TODO this is only necessary for successive shortest paths
# Dijkstra's shortest paths for a modified Hungarian algorithm
# returns a path of least cost from source to sink, given as a list of
# edges (u, v)
def dijkstra(G, F, source, sink):
	# number of vertices
	n = len(G)
	# initialize
	dist = [sys.maxint for i in xrange(n)]
	paths = {source: []}
	dist[source] = 0
	# priority queue as a dictionary
	heap = {source: 0}
	# keep approximating distance until all paths tried
	while heap:
		u = min(heap, key=heap.get)
		del heap[u]
		for v in G[u].keys():
			if G[u][v][0] - F[u][v] > 0:
				tempdist = sys.maxint
				if dist[u] != sys.maxint:
					tempdist = dist[u] + G[u][v][1]
				if dist[v] > tempdist:
					dist[v] = tempdist
					paths[v] = paths[u] + [(u,v)]
					heap[v] = dist[v]
	return paths[sink]