import sys
from sys import stdin

g = [{1: (0, 1), 2: (0, 10)},{2: (0, 100), 3: (0, 100)},{3: (0, 1)},{}]
g2 = [{3: (1,1), 4: (1,2)},{3: (1,1), 4: (1,2)},{3: (1,1), 4: (1,50)},{6: (2,0)},{6:(1,0)},{0: (1,0), 1: (1,0), 2: (1,0)},{}]

def dijkstra(graph, start, end):
	# number of vertices
	n = len(graph)

	# initialize
	dist = [sys.maxint for i in xrange(n)]
	paths = {start: []}
	dist[start] = 0

	# priority queue as a dictionary
	heap = {start: 0}

	while heap:
		u = min(heap, key=heap.get)
		del heap[u]
		for v in graph[u].keys():
			tempdist = sys.maxint
			if dist[u] != sys.maxint:
				tempdist = dist[u] + graph[u][v][1]
			if dist[v] > tempdist:
				dist[v] = tempdist
				paths[v] = paths[u] + [(u,v)]
				heap[v] = dist[v]

	return paths[end]

print dijkstra(g2, 5, 6)