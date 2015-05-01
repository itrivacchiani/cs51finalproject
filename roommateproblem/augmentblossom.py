# given blossom b and vertex v switch out matched and unmatched edges between them
def augment_blossom(b, v):
    t = v
    while parents[t] != b:
        t = parents[t]
    if isinstance(t, Blossom):
        augment_blossom(t, v)
    indx1 = indx2 = b.subblossoms.index(t)

    # determine direction
    if indx1 % 2 == 1:
        indx2 -= len(b.subblossoms)
        direc = 1
    else:
        direc = -1

    # find base
    while indx2 != 0:
        indx2 += direc
        t = b.subblossoms[indx2]
        if direc == 1:
            w, x = b.edges[indx2]
        else:
            x, w = b.edges[indx2-1]
        if isinstance(t, Blossom):
            augment_blossom(t, w)
        indx2 += direc
        t = b.subblossoms[indx2]
        if isinstance(t, Blossom):
            augment_blossom(t, x)
        (roommates[w], roommates[x]) = (x, w)

    # repositioning for new base
    b.subblossoms = b.subblossoms[indx1:] + b.subblossoms[:indx1]
    b.edges  = b.edges[indx1:]  + b.edges[:indx1]
    bases[b] = bases[b.subblossoms[0]]