# edge slack
def slack(v, w):
    return vdual[v] + vdual[w] - 2 * G.get_edge(v, w)