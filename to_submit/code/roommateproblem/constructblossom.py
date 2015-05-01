# constructs blossom through the given S-vertices v,w with given base
def construct_blossom(base, v, w):
    (rootb, rootv, rootw) = (root[base], root[v], root[w])
    b = Blossom()
    (bases[b], parents[b], parents[rootb]) = (base, None, b)
    b.subblossoms = path = []
    b.edges  = edgs = [(v, w)]

    # trace from v to base.
    while rootv != rootb:
        parents[rootv] = b
        path.append(rootv)
        edgs.append(elbl[rootv])
        v = elbl[rootv][0]
        rootv = root[v]
    path.append(rootb)
    path.reverse()
    edgs.reverse()

    # trace from w to base.
    while rootw != rootb:
        parents[rootw] = b
        path.append(rootw)
        edgs.append((elbl[rootw][1], elbl[rootw][0]))
        w = elbl[rootw][0]
        rootw = root[w]
    (lbl[b],elbl[b], bdual[b]) = (1, elbl[rootb], 0)
    
    # relabeling
    for v in b.lvertices():
        if lbl[root[v]] == 2:
            Svertexqueue.append(v)
        root[v] = b

    # calculate out leastslackedges
    bestedgeto = {}
    for epath in path:
        if isinstance(epath, Blossom):
            if epath.leastslackedges is not None:
                lslack = epath.leastslackedges
                epath.leastslackedges = None
            else:
                lslack = [(v, w) for v in epath.lvertices() for w in G.neighbors(v) if v != w]
        else:
            lslack = [(epath, w) for w in G.neighbors(epath) if epath != w]
        for k in lslack:
            (i, j) = k
            if root[j] == b:
                i, j = j, i
            bj = root[j]
            if (bj != b and lbl.get(bj) == 1 and ((bj not in bestedgeto) or edgeslack(i, j) < edgeslack(*bestedgeto[bj]))):
                bestedgeto[bj] = k
        leastslack[epath] = None
    b.leastslackedges = bestedgeto.values()

    # pick out the optimal edge
    opt = None
    leastslack[b] = None
    for e in b.leastslackedges:
        es = edgeslack(*e)
        if opt is None or es < optedgeslack:
            opt = e
            optedgeslack = es
    leastslack[b] = opt