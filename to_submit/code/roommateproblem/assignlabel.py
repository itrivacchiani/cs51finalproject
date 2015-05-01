# given vertices v, w and label t, assign t to the top-level blossom 
# that contains w and comes through an edge from v
def assign_label(w, t, v):
    lbl[w] = lbl[root[w]] = t
    if v is not None:
        elbl[w] = (v, w)
        elbl[root[w]] = (v, w)
    else:
        elbl[w] = None
        elbl[root[w]] = None
    leastslack[w] = None
    leastslack[root[w]] = None
    if t == 1:
        if isinstance(root[w], Blossom):
            Svertexqueue.extend(root[w].lvertices())
        else:
            Svertexqueue.append(root[w])
    elif t == 2:
        base = bases[root[w]]
        assign_label(roommates[base], 1, base)