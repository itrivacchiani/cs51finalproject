# computes the optimal matchings in the roommate problem
def find_maximum_matching():
    label.clear()
    labeledge.clear()
    bestedge.clear()
    for b in bdual:
        b.leastslackedges = None
    allowedge.clear()
    queue[:] = []

    # label single blossoms and vertices S and enqueue
    for v in gnodes:
        if (v not in roommates) and label.get(root[v]) is None:
            assign_label(v, 1, None)
    if find_augmenting_path():
        for b in bdual.keys():
            if b not in bdual:
                continue
            if (parents[b] is None and label.get(b) == 1 and bdual[b] == 0):
                lift_blossom(b, True)
        find_maximum_matching()