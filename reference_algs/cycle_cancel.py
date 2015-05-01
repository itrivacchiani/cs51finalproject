# cycle cancel attempt 2

import sys

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
	return (F, maxflow)

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
	cycle = []
	for u in xrange(n):
		for v in graph[u].keys():
			if dist[v] > dist[u] + graph[u][v][1]:
				temp = (u,v)
				while temp not in cycle:
					cycle.append(temp)
					temp = (prev[temp[0]],temp[0])
				return cycle
	# no negative cycles
	return None

def cycle_cancel(G, source, sink):
	n = len(G)

	# feasible flow
	F, maxflow, matching = edmonds_karp(G, source, sink)

	# remove used flow edges in F
	for u in xrange(n):
		for v in G[u].keys():
			if F[u][v][0] > 0:
				F[u][v] = (0,0)

	# add unused edges from G to F
	for u in xrange(n-2):
		for v in G[u].keys():
			if F[v][u] == (0,0):
				F[u][v] = G[u][v]

	# convert now residual graph F into list of dicts
	resG = [{} for i in xrange(n)]
	for u in xrange(n):
		for v in xrange(n):
			if F[u][v] != (0, 0):
				resG[u][v] = (abs(F[u][v][0]), F[u][v][1])
	
	# TODO use Bellman-Ford to find cycles from sink in residual graph
	# augment along this cycle and keep doing so until no more cycles
	# rewrite Bellman-Ford to return path of negative cycle
	# sink becomes source in residual graph
	while True:
		cycle = bellman_ford(resG, sink)
		if not cycle:
			break
		# smallest capacity of the cycle
		flow = min(resG[u][v][0] for u,v in cycle)
		# agument along cycle, updating flow graph and TODO residual graph
		for u,v in cycle:
			#F[u][v] = (F[u][v][0] + flow, F[u][v][1])
			#F[v][u] = (F[v][u][0] - flow, F[v][u][1])
			temp = resG[u][v]
			# update reverse edge
			if u in resG[v].keys():
				resG[v][u] = (resG[v][u][0] + flow, resG[v][u][1])
			else:
				resG[v][u] = (flow, -resG[u][v][1])
			# update forward edge
			if temp[0] == flow:
				# remove edge if no more capacity
				del resG[u][v]
			else:
				resG[u][v] = (resG[u][v][0] - flow, resG[u][v][1])

		# TODO updating correctly?
		#for u in resG:
		#	print u

	cost = 0
	assignment = {}
	# initialize all demand nodes
	for v in resG[sink].keys():
		assignment[v] = []
	for u in xrange(n):
		for v in resG[u].keys():
			edge = resG[u][v]
			if edge[1] < 0:
				cost -= edge[1]
				assignment[u].append(v)

	return maxflow, cost, assignment

# Testing

# g = [{3: (1,1), 4: (1,2)},{3: (1,1), 4: (1,2)},{3: (1,1), 4: (1,50)},{6: (2,0)},{6:(1,0)},{0: (1,0), 1: (1,0), 2: (1,0)},{}]

# maxflow, cost, assignment = cycle_cancel(g, 5, 6)

# print maxflow
# print cost
# print assignment