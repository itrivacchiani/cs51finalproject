# finds augmenting path or blossom to recurse on
def find_augmenting_path2(v, w):
    path = []
    base = Dummy
    while v is not Dummy:
        b = root[v]
        if lbl[b] & 4:
            base = bases[b]
            break
        path.append(b)
        lbl[b] = 5
        if elbl[b] is None:
            v = Dummy
        else:
            v = elbl[b][0]
            b = root[v]
            v = elbl[b][0]
        if w is not Dummy:
            v, w = w, v
    for b in path:
        lbl[b] = 1
    return base