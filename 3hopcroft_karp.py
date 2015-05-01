# Hopcroft-Karp for max cardinality bipartite matching
# Outputs a dictionary mapping elements of the first list X to
# ones in the second list Y
# A is the matched elements from X; B is the matched elements from Y
def hopcroft_karp(graph):
	# number of vertices, source and sink nodes are irrelevant
	n = len(graph) - 2

	# find a working matching, to fix later
	matching = {}
	for u in xrange(len(n)):
		for v in graph[u].keys():
			if v not in matching:
				matching[v] = u
				break

	# try to correct the matching to have disjoint edges
	while True:
		# residual graph is constructed in layers
		# list of connected vertices from previous matching in Y
		prevY = {}
		# unmatched vertices in final matching of Y
		unmatched = []
		# connected vertices from previous matching
		prevX = dict([(u,unmatched) for u in xrange(n)])
		for v in matching:
			del prevX[matching[v]]
		layer = list(prevX)

		# keep extending layering structure two at a time
		while layer and not unmatched:
			newLayer = {}
			for u in layer:
				for v in graph[u].keys():
					if v not in prevY:
						newLayer.setdefault(v,[]).append(u)
			layer = []
			for v in newLayer:
				prevY[v] = newLayer[v]
				if v in matching:
					layer.append(matching[v])
					prevX[matching[v]] = v
				else:
					unmatched.append(v)

		# check if done layering
		if not unmatched:
			unlayered = {}
			for u in xrange(n):
				for v in graph[u].keys():
					if v not in prevY:
						unlayered[v] = None
			return (matching,list(prevX),list(unlayered))

		# recursively check through remembered layers for alternating paths
		def recurse(v):
			if v in prevY:
				L = prevY[v]
				del prevY[v]
				for u in L:
					if u in prevX:
						prevX_u = prevX[u]
						del prevX[u]
						if prevX_u is unmatched or recurse(prevX_u):
							matching[v] = u
							return True
			return False
		for v in unmatched:
			recurse(v)