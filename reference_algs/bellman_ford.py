import sys
from sys import stdin

posg = [{1: (0, 1), 2: (0, 10)},{2: (0, 100), 3: (0, 100)},{3: (0, 1)},{}]

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

	return dist, prev