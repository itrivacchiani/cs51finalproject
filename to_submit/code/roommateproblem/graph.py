# graph class

class Graph(object):
    nodes = []
    edges = []
    nodemap = {}
    edgemap = {}
    def add_edge(self,v,w,k):
        if v in self.nodes:
            self.nodemap[v].append(w)
        else:
            self.nodemap[v] = [w]
        if w in self.nodes:
            self.nodemap[w].append(v)
        else:
            self.nodemap[w] = [v]
        if v not in self.nodes:
            self.nodes.append(v)
        if w not in self.nodes:
            self.nodes.append(w)
        self.edges.append((v,w,k))
        self.edgemap[(v,w)] = k
        self.edgemap[(w,v)] = k
        return
    def get_edge(self,v,w):
        return self.edgemap[(v,w)]
    def neighbors(self,v):
        return self.nodemap[v]