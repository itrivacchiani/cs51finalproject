# lifts a given toplevel blossom
def lift_blossom(b, endstage):
    # iterate through subblossoms and convert them into toplevel blossoms
    for s in b.subblossoms:
        parents[s] = None
        if isinstance(s, Blossom):
            if endstage and bdual[s] == 0:
                lift_blossom(s, endstage)
            else:
                for v in s.leaves():
                    root[v] = s
        else:
            root[s] = s

    # relabeling subblossoms until reach base
    if (not endstage) and label.get(b) == 2:
        entrychild = root[labeledge[b][1]]
        j = b.subblossoms.index(entrychild)
        if j % 2 == 1:
            j -= len(b.subblossoms)
            jstep = 1
        else:
            jstep = -1
        v, w = labeledge[b]
        while j != 0:
            if jstep == 1:
                p, q = b.edges[j]
            else:
                q, p = b.edges[j-1]
            label[w] = None
            label[q] = None
            assign_label(w, 2, v)
            allowedge[(p, q)] = allowedge[(q, p)] = True
            j += jstep
            if jstep == 1:
                v, w = b.edges[j]
            else:
                w, v = b.edges[j-1]
            allowedge[(v, w)] = allowedge[(w, v)] = True
            j += jstep
        bw = b.subblossoms[j]
        label[w] = label[bw] = 2
        labeledge[w] = labeledge[bw] = (v, w)
        bestedge[bw] = None
        j += jstep
        while b.subblossoms[j] != entrychild:
            bv = b.subblossoms[j]
            if label.get(bv) == 1:
                j += jstep
                continue
            if isinstance(bv, Blossom):
                for v in bv.leaves():
                    if label.get(v):
                        break
            else:
                v = bv
            if label.get(v):
                label[v] = None
                label[roommates[bases[bv]]] = None
                assign_label(v, 2, labeledge[v][0])
            j += jstep

    # gets rid of lifted blossom
    label.pop(b, None)
    labeledge.pop(b, None)
    bestedge.pop(b, None)
    del parents[b]
    del bases[b]
    del bdual[b]