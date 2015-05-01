import sys
from sys import stdin

posg = [{1: (0, 1), 2: (0, 10)},{2: (0, 100), 3: (0, 100)},{3: (0, 1)},{}]

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
			if G[u][v][0] - F[u][v][0] > 0:
				tempdist = sys.maxint
				if dist[u] != sys.maxint:
					tempdist = dist[u] + G[u][v][1]
				if dist[v] > tempdist:
					dist[v] = tempdist
					paths[v] = paths[u] + [(u,v)]
					heap[v] = dist[v]
	if sink not in paths:
		return -1
	else:
		return paths[sink]

def bellman_ford(graph, source):
	# number of vertices
	n = len(graph)

	# initialize output arrays
	dist = [sys.maxint for i in xrange(n)]
	prev = [-1 for i in xrange(n)]
	dist[source] = 0
	prev[source] = source

	for i in xrange(n-1):
		for u in xrange(n):
			for v in graph[u].keys():
				tempdist = sys.maxint
				if dist[u] != sys.maxint:
					tempdist = dist[u] + graph[u][v][1]
				if dist[v] > tempdist:
					dist[v] = tempdist
					prev[v] = u

	# Return 0 if negative-weight cycles
	for u in xrange(n):
		for v in graph[u].keys():
			if dist[v] > dist[u] + graph[u][v][1]:
				return 0

	return dist

def SSP(G, source, sink):
	# number of vertices
	n = len(G)

	# residual graph, with flows and capacities
	F = [[(0, 0)] * n for i in xrange(n)]

	potentials = bellman_ford(G, source)
	print potentials
	# reduce cost on potentials
	# reducing costs and updating node potentials
	def reduce_cost(G, F, potentials):
		for u in xrange(n):
			for v in G[u].keys():
				F[u][v] = (F[u][v][0], F[u][v][1] + potentials[u] - potentials[v])
				F[v][u] = (F[v][u][0], 0)
		return F
	F = reduce_cost(G, F, potentials)

	while True:
		path = dijkstra(G, F, source, sink)
		# no more paths from s to t
		if path == -1:
			break
		print path
		F = reduce_cost(G, F, potentials)
		print F
		# traverse path to find smallest capacity
		flow = min(G[u][v][0] - F[u][v][0] for u,v in path)
		# traverse path to update flow
		for u,v in path:
			F[u][v] = (F[u][v][0] + flow, F[u][v][1])
			F[v][u] = (F[v][u][0] - flow, F[v][u][1])

	totalflow = sum(F[source][i][0] for i in xrange(n))
	assignment = {}
	cost = 0
	for x in xrange(len(F[source])):
		if F[source][x][0] > 0:
			for y in xrange(len(F[x])):
				if F[x][y][0] > 0:
					cost += G[x][y][1]
					if y not in assignment:
						assignment[y] = [x]
					else:
						assignment[y].append(x)
	return (totalflow, cost, assignment)

g = [{3: (1,1), 4: (1,2)},{3: (1,1), 4: (1,2)},{3: (1,1), 4: (1,50)},{6: (2,0)},{6:(1,0)},{0: (1,0), 1: (1,0), 2: (1,0)},{}]

print SSP(g, 5, 6)