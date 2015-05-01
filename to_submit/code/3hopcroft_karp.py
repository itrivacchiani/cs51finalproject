import csv, os

# Hopcroft-Karp for max cardinality bipartite matching
# Outputs a dictionary mapping elements of the first list X to
# ones in the second list Y
# A is the matched elements from X; B is the matched elements from Y
def hopcroft_karp(graph):
	# number of vertices, source and sink nodes are irrelevant
	n = len(graph)

	# find a working matching, to fix later
	matching = {}
	for u in xrange(n):
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


#######################################################
# I/O

data = open('bipartitegraph.csv')
csv_f = csv.reader(data)

problem = csv_f.next()[0].lower()
# csv file does not correctly indicate stable marriage or 
# hospital resident as the problem to be solved
if problem != "maximum cardinality bipartite matching":
	print "The problem indicated in graph.csv is not maximum cardinality bipartite matching\n"
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
	neighborindices = [vertexnames.index(elt) for elt in s1.split(' ')]
	for v in xrange(len(neighborindices)):
		graph[vertexindex][neighborindices[v]] = (0,0)

# assume source and sink already added, last two vertices
source = numVertices - 2
sink = source + 1

matching, A, B = hopcroft_karp(graph)

print "\nSolution:"
for a in matching.keys():
	print "%s <--> %s" % (vertexnames[a], vertexnames[matching[a]])

data.close()
os.system("python menu.py")