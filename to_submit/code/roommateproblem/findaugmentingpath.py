# finds an augmenting path in G
# returns 0 if no path is found
def find_augmenting_path():
    pathfound = 0
    while 1:
        while queue and not pathfound:
            v = queue.pop()
            for w in G.neighbors(v):
                if root[v] == root[w] or w == v:
                    continue
                if (v, w) not in allowedge:
                    kslack = slack(v, w)
                    if kslack <= 0:
                        allowedge[(v, w)] = allowedge[(w, v)] = True
                if (v, w) in allowedge:
                    if label.get(root[w]) is None:
                        assign_label(w, 2, v)
                    elif label.get(root[w]) == 1:
                        base = find_augmenting_path2(v, w)
                        if base is not Dummy:
                            construct_blossom(base, v, w)
                        else:
                            augment_matching(v, w)
                            pathfound = 1
                            break
                    elif label.get(w) is None:
                        label[w] = 2
                        labeledge[w] = (v, w)
                elif label.get(root[w]) == 1:
                    if bestedge.get(root[v]) is None or kslack < slack(*bestedge[root[v]]):
                        bestedge[root[v]] = (v, w)
                elif label.get(w) is None:
                    if bestedge.get(w) is None or kslack < slack(*bestedge[w]):
                        bestedge[w] = (v, w)
        if pathfound:
            break

        # tracker of the occurence of the minimum delta
        deltatype = 1

        # minimum of the dual variables corresponding to the vertices
        delta = min(vdual.values())
        deltaedge = deltablossom = None

        # minimum edge slack between S-vertex and free vertex
        for v in G.nodes:
            if label.get(root[v]) is None and bestedge.get(v) is not None:
                d = slack(*bestedge[v])
                if deltatype == -1 or d < delta:
                    delta = d
                    deltatype = 2
                    deltaedge = bestedge[v]

        # minimum edge slack between any two S-blossoms
        for b in parents:
            if (parents[b] is None and label.get(b) == 1 and bestedge.get(b) is not None):
                kslack = slack(*bestedge[b])
                d = kslack / 2
                if deltatype == -1 or d < delta:
                    delta = d
                    deltatype = 3
                    deltaedge = bestedge[b]

        # minimum dual variable corresponding to a T-blossom
        for b in bdual:
            if (parents[b] is None and label.get(b) == 2 and (deltatype == -1 or bdual[b] < delta)):
                delta = bdual[b]
                deltatype = 4
                deltablossom = b

        # maximum cardinality attained
        if deltatype == -1:
            deltatype = 1
            delta = max(0, min(vdual.values()))

        # update dual program variables
        for v in gnodes:
            vdual[v] = {None: lambda x:x,
                          1: lambda x: x-delta,
                          2: lambda x: x+delta}[label.get(root[v])](vdual[v])
        for b in bdual:
            if parents[b] is None:
                bdual[b] = {None: lambda x:x,
                                  1: lambda x: x+delta,
                                  2: lambda x: x-delta}[label.get(b)](bdual[b])

        # switch statement for the occurence of the minimum delta
        if deltatype == 1: 
            break
        elif deltatype == 2 or deltatype == 3:
            (v, w) = deltaedge
            allowedge[(v, w)] = allowedge[(w, v)] = True
            queue.append(v)
        elif deltatype == 4:
            lift_blossom(deltablossom, False)
    return pathfound