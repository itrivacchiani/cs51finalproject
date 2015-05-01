# finds augmenting path or blossom to recurse on
def find_augmenting_path2(v, w):
    path = []
    base = Dummy
    while v is not Dummy:
        b = root[v]
        if label[b] & 4:
            base = bases[b]
            break
        path.append(b)
        label[b] = 5
        if labeledge[b] is None:
            v = Dummy
        else:
            v = labeledge[b][0]
            b = root[v]
            v = labeledge[b][0]
        if w is not Dummy:
            v, w = w, v
    for b in path:
        label[b] = 1
    return base