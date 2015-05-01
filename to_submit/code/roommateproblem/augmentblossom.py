# given blossom b and vertex v switch out matched and unmatched edges between them
def augment_blossom(b, v):
    t = v
    while parents[t] != b:
        t = parents[t]
    if isinstance(t, Blossom):
        augment_blossom(t, v)
    i = j = b.subblossoms.index(t)

    # determine direction
    if i % 2 == 1:
        j -= len(b.subblossoms)
        jstep = 1
    else:
        jstep = -1

    # find base
    while j != 0:
        j += jstep
        t = b.subblossoms[j]
        if jstep == 1:
            w, x = b.edges[j]
        else:
            x, w = b.edges[j-1]
        if isinstance(t, Blossom):
            augment_blossom(t, w)
        j += jstep
        t = b.subblossoms[j]
        if isinstance(t, Blossom):
            augment_blossom(t, x)
        (roommates[w], roommates[x]) = (x, w)

    # repositioning for new base
    b.subblossoms = b.subblossoms[i:] + b.subblossoms[:i]
    b.edges  = b.edges[i:]  + b.edges[:i]
    bases[b] = bases[b.subblossoms[0]]