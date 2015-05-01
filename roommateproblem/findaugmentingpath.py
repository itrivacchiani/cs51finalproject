# finds an augmenting path in G
# returns 0 if no path is found
def find_augmenting_path():
    pathfound = 0
    while 1:
        while Svertexqueue and not pathfound:
            v = Svertexqueue.pop()
            for w in G.neighbors(v):
                if root[v] == root[w] or w == v:
                    continue
                if (v, w) not in zeroslack:
                    kslack = edgeslack(v, w)
                    if kslack <= 0:
                        zeroslack[(v, w)] = zeroslack[(w, v)] = True
                if (v, w) in zeroslack:
                    if lbl.get(root[w]) is None:
                        assign_label(w, 2, v)
                    elif lbl.get(root[w]) == 1:
                        base = find_augmenting_path2(v, w)
                        if base is not Dummy:
                            construct_blossom(base, v, w)
                        else:
                            augment_matching(v, w)
                            pathfound = 1
                            break
                    elif lbl.get(w) is None:
                        lbl[w] = 2
                        elbl[w] = (v, w)
                elif lbl.get(root[w]) == 1:
                    if leastslack.get(root[v]) is None or kslack < edgeslack(*leastslack[root[v]]):
                        leastslack[root[v]] = (v, w)
                elif lbl.get(w) is None:
                    if leastslack.get(w) is None or kslack < edgeslack(*leastslack[w]):
                        leastslack[w] = (v, w)
        if pathfound:
            break

        # tracker of the occurence of the min track
        tracker = 1

        # minimum of the dual variables corresponding to the vertices
        track = min(vdual.values())
        etracker = btracker = None

        # minimum edge slack between S-vertex and free vertex
        for v in G.nodes:
            if lbl.get(root[v]) is None and leastslack.get(v) is not None:
                d = edgeslack(*leastslack[v])
                if tracker == -1 or d < track:
                    track = d
                    tracker = 2
                    etracker = leastslack[v]

        # minimum edge slack between any two S-blossoms
        for b in parents:
            if (parents[b] is None and lbl.get(b) == 1 and leastslack.get(b) is not None):
                kslack = edgeslack(*leastslack[b])
                d = kslack / 2
                if tracker == -1 or d < track:
                    track = d
                    tracker = 3
                    etracker = leastslack[b]

        # minimum dual variable corresponding to a T-blossom
        for b in bdual:
            if (parents[b] is None and lbl.get(b) == 2 and (tracker == -1 or bdual[b] < track)):
                track = bdual[b]
                tracker = 4
                btracker = b

        # maximum cardinality attained
        if tracker == -1:
            tracker = 1
            track = max(0, min(vdual.values()))

        # update dual program variables
        for v in G.nodes:
            vdual[v] = {None: lambda x:x,
                          1: lambda x: x-track,
                          2: lambda x: x+track}[lbl.get(root[v])](vdual[v])
        for b in bdual:
            if parents[b] is None:
                bdual[b] = {None: lambda x:x,
                                  1: lambda x: x+track,
                                  2: lambda x: x-track}[lbl.get(b)](bdual[b])

        # switch statement for the occurence of the min track
        if tracker == 1: 
            break
        elif tracker == 2 or tracker == 3:
            (v, w) = etracker
            zeroslack[(v, w)] = zeroslack[(w, v)] = True
            Svertexqueue.append(v)
        elif tracker == 4:
            lift_blossom(btracker, False)
    return pathfound