import csv, os
import edmond_karp

# I/O
data = open('graph.csv')
csv_f = csv.reader(data)

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

F, maxflow, matching = edmond_karp.edmonds_karp(graph, source, sink)

print "\nSolution:"
print "flow = %i" % maxflow
print "Matching:"
for a in matching.keys():
	print "%s <--> %s" % (vertexnames[a], vertexnames[matching[a]])

data.close()
os.system("python menu.py")