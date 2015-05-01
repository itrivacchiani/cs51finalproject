# given vertices v, w and label t, assign t to the top-level blossom 
# that contains w and comes through an edge from v
def assign_label(w, t, v):
    label[w] = label[root[w]] = t
    if v is not None:
        labeledge[w] = labeledge[root[w]] = (v, w)
    else:
        labeledge[w] = labeledge[root[w]] = None
    bestedge[w] = bestedge[root[w]] = None
    if t == 1:
        if isinstance(root[w], Blossom):
            queue.extend(root[w].leaves())
        else:
            queue.append(root[w])
    elif t == 2:
        base = bases[root[w]]
        assign_label(roommates[base], 1, base)