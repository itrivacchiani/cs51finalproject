import copy, sys, csv, os
import 9edmond_karp

# Bellman-Ford for detecting negative cycles for use in Cycle-Cancelling alg
# if no negative cycles, return None
def bellman_ford(graph, source):
	# number of vertices
	n = len(graph)

	# initialize output arrays
	dist = [sys.maxint for i in xrange(n)]
	prev = [-1 for i in xrange(n)]
	dist[source] = 0
	prev[source] = source

	# do |V| - 1 relaxations
	for i in xrange(n-1):
		for u in xrange(n):
			for v in graph[u].keys():
				tempdist = sys.maxint
				if dist[u] != sys.maxint:
					tempdist = dist[u] + graph[u][v][1]
				if dist[v] > tempdist:
					dist[v] = tempdist
					prev[v] = u

	# find and return a cycle as a list of pairs of vertices
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

# Cycle-Cancelling algorithm solves min cost max flow
# after finding a suitable maxflow, fixes it to minimal cost by augmenting along
# the negative cost cycles
# Returns the maxflow, cost, and the assignment as a dictionary
# the assignment is given as a dictionary; it assumes a bipartite graph,
# even though the algorithm works for general networks
def cycle_cancel(G, source, sink):
	# number of vertices
	n = len(G)

	# find feasible maxflow
	F, maxflow, matching = 9edmond_karp.edmonds_karp(G, source, sink)

	# convert flow graph the from the maxflow to a residual graph
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
	
	# use Bellman-Ford to find cycles reachable from sink in residual graph
	# augment along this cycle and keep doing so until no more cycles
	while True:
		cycle = bellman_ford(resG, sink)
		if not cycle:
			break
		# smallest capacity of the cycle
		flow = min(resG[u][v][0] for u,v in cycle)
		# agument along cycle, updating flow graph and TODO residual graph
		for u,v in cycle:
			# update residual graph
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

#######################################################
# I/O
csv_f = csv.reader(open('graph.csv'))

problem = csv_f.next()[0].lower()
# csv file does not correctly indicate stable marriage or 
# hospital resident as the problem to be solved
if problem != "min cost max flow":
	print "The problem indicated in graph.csv is not min cost max flow\n"
	print "Exiting to menu."
	os.system("python menu.py")

numVertices = int(csv_f.next()[0])
# initialize graph
graph = [{} for i in xrange(numVertices)]
vertexnames = csv_f.next()[0].split(' ')

for i in xrange(numVertices):
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

maxflow, cost, assignment = cycle_cancel(graph, source, sink)

print "\nSolution:"
print "cost = %i" % cost
print "Assignment:"
for v in assignment.keys():
	print [vertexnames[u] for u in assignment[v]]
	print "assigned to: %s" % vertexnames[v]

os.system("python menu.py")