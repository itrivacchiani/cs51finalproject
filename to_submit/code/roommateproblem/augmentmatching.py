# given two S-vertices v and w switch out matched and unmatched edges between them
def augment_matching(v, w):
    for (s, t) in ((v, w), (w, v)):
        while 1:
            if isinstance(root[s], Blossom):
                augment_blossom(root[s], s)
            roommates[s] = t
            if elbl[root[s]] is None:
                break
            u = elbl[root[s]][0]
            s, t = elbl[root[u]]
            if isinstance(root[u], Blossom):
                augment_blossom(root[u], t)
            roommates[t] = s