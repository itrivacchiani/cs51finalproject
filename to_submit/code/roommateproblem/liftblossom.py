# lifts a given toplevel blossom
def lift_blossom(b, es):
    # iterate through subblossoms and convert them into toplevel blossoms
    for s in b.subblossoms:
        parents[s] = None
        if isinstance(s, Blossom):
            if es and bdual[s] == 0:
                lift_blossom(s, es)
            else:
                for v in s.lvertices():
                    root[v] = s
        else:
            root[s] = s

    # relabeling subblossoms until reach base
    if (not es) and lbl.get(b) == 2:
        ec = root[elbl[b][1]]
        indx = b.subblossoms.index(ec)
        if indx % 2 == 0:
            direc = -1
        else:
            indx -= len(b.subblossoms)
            direc = 1
        v, w = elbl[b]
        while indx != 0:
            if direc == -1:
                (q, p) = b.edges[indx-1]
            else:
                (p, q) = b.edges[indx]
            (lbl[w], lbl[q]) = (None, None)
            assign_label(w, 2, v)
            zeroslack[(p, q)] = zeroslack[(q, p)] = True
            indx += direc
            if direc == 1:
                (v, w) = b.edges[indx]
            else:
                (w, v) = b.edges[indx-1]
            zero[(v, w)] = zeroslack[(w, v)] = True
            indx += direc
        subx = b.subblossoms[indx]
        elbl[w] = (v, w)
        elbl[subx] = (v, w)
        lbl[w] = 2
        lbl[subx] = 2
        leastslack[subx] = None
        indx += direc
        while b.subblossoms[indx] != ec:
            subx2 = b.subblossoms[indx]
            if lbl.get(subx2) == 1:
                indx += direc
                continue
            if isinstance(subx2, Blossom):
                for v in subx2.lvertices():
                    if lbl.get(v):
                        break
            else:
                v = subx2
            if lbl.get(v):
                (lbl[v], lbl[roommates[bases[subx2]]]) = (None, None)
                assign_label(v, 2, elbl[v][0])
            indx += direc

    # gets rid of lifted blossom
    lbl.pop(b, None)
    elbl.pop(b, None)
    leastslack.pop(b, None)
    del parents[b], bases[b], bdual[b]