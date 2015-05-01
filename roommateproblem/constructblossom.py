# constructs blossom through the given S-vertices v,w with given base
def construct_blossom(base, v, w):
    (bb, bv, bw) = (root[base], root[v], root[w])
    b = Blossom()
    (bases[b], parents[b], parents[bb]) = (base, None, b)
    b.subblossoms = path = []
    b.edges  = edgs = [(v, w)]

    # trace from v to base.
    while bv != bb:
        parents[bv] = b
        path.append(bv)
        edgs.append(labeledge[bv])
        v = labeledge[bv][0]
        bv = root[v]
    path.append(bb)
    path.reverse()
    edgs.reverse()

    # trace from w to base.
    while bw != bb:
        parents[bw] = b
        path.append(bw)
        edgs.append((labeledge[bw][1], labeledge[bw][0]))
        w = labeledge[bw][0]
        bw = root[w]
    (label[b],labeledge[b], bdual[b]) = (1, labeledge[bb], 0)
    
    # relabeling
    for v in b.leaves():
        if label[root[v]] == 2:
            queue.append(v)
        root[v] = b

    # calculate out leastslackedges
    bestedgeto = {}
    for bv in path:
        if isinstance(bv, Blossom):
            if bv.leastslackedges is not None:
                nblist = bv.leastslackedges
                bv.leastslackedges = None
            else:
                nblist = [(v, w) for v in bv.leaves() for w in G.neighbors_iter(v) if v != w]
        else:
            nblist = [(bv, w) for w in G.neighbors_iter(bv) if bv != w]
        for k in nblist:
            (i, j) = k
            if root[j] == b:
                i, j = j, i
            bj = root[j]
            if (bj != b and label.get(bj) == 1 and ((bj not in bestedgeto) or slack(i, j) < slack(*bestedgeto[bj]))):
                bestedgeto[bj] = k
        bestedge[bv] = None
    b.leastslackedges = bestedgeto.values()

    # pick out the best edge
    mybestedge = None
    bestedge[b] = None
    for k in b.leastslackedges:
        kslack = slack(*k)
        if mybestedge is None or kslack < mybestslack:
            mybestedge = k
            mybestslack = kslack
    bestedge[b] = mybestedge