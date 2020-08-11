import queue

def get_accessible_nodes(adj, source, valid_nodes):
    n = adj.shape[0]
    q = queue.Queue(maxsize=n)
    seen = [False] * n

    q.put(source)
    seen[source] = True

    while not q.empty():
        node = q.get()
        for i in valid_nodes:
            if adj[node, i] and seen[i] is False:
                q.put(i)
                seen[i] = True
    res = []
    for i in range(n):
        if seen[i]:
            res.append(i)

    return res


def bfs_optimized(neighbors, start):
    n = len(neighbors)
    q = queue.Queue()
    seen = {i: False for i in neighbors.keys()}
    seen[start] = True
    q.put(start)
    while not q.empty():
        node = q.get()
        for i in neighbors[node]:
            if not seen[i]:
                q.put(i)
                seen[i] = True

    res = []
    for i in seen:
        if seen[i]:
            res.append(i)

    return set(res)



def set_root(adj_mat, neighbors, root, is_valid):

    added_edges = []
    q = queue.Queue()


    for i in neighbors[root]:
        if is_valid[i] and adj_mat[root][i] == 1 and adj_mat[i][root] == 1:
            added_edges.append((root, i))
            q.put((root, i))
            adj_mat[i][root] = 0

    """
    If the graph is not chordal, direction of the root's edges might be overwritten in the following while-loop! 
    """
    while not q.empty():
        s, e = q.get()
        for i in neighbors[e]:
            if is_valid[i] and adj_mat[e][i] == 1 and adj_mat[i][e] == 1 and adj_mat[s][i] == 0 and adj_mat[i][s] == 0:
                added_edges.append((e, i))
                q.put((e, i))
                adj_mat[i][e] = 0

    return added_edges



fact = [1] * 5000
for i in range(1,5000):
    fact[i] = fact[i-1] * i


def separate_graph(G):
    for i in G:
        for j in G[i].copy():
            if not i in G[j]:
                G[i].remove(j)
    left=set(G.keys())
    H=[]
    while len(left)>0:
        current=left.pop()
        visited={current}
        tovisit=G[current].copy()
        Tg={}
        Tg[current]=G[current].copy()
        while len(tovisit)>0:
            tem=tovisit.pop()
            visited.add(tem)
            Tg[tem]=G[tem].copy()
            tovisit.update(G[tem].difference(visited))
            left.remove(tem)
        H.append(Tg)
    return H


def set_root_optimized(root, neighbors):
    nodes = set(neighbors.keys())
    directed_edges = []

    if root not in nodes:
        print("Missing root!")

    current_nodes = {root}
    CCs = list()
    left = nodes - current_nodes

    while len(left) != 0:
        res = set()
        fathers = {}
        for i in current_nodes:
            nodestem = neighbors[i].intersection(left)
            res |= nodestem
            for nodesi in nodestem:
                if nodesi in fathers:
                    fathers[nodesi].add(i)
                else:
                    fathers[nodesi] = {i}
                directed_edges.append((i, nodesi))
        residual_graph = {i: neighbors[i]&res for i in res}

        is_done = False
        while not is_done:
            is_done = True
            for i in residual_graph:
                removed_edges = []
                for j in residual_graph[i]:
                    if not fathers[i].issubset(neighbors[j]):
                        fathers[j].add(i)
                        removed_edges.append((i, j))
                        directed_edges.append((i, j))
                        is_done = False
                for x, y in removed_edges:
                    residual_graph[x].remove(y)
                    residual_graph[y].remove(x)

            residual_graph = {i:residual_graph[i] for i in residual_graph}
        CCs.extend(separate_graph(residual_graph))
        if len(res) == 0:
            break
        current_nodes = res
        left -= res

    new_neighbors = {i: set() for i in nodes}
    for x, y in directed_edges:
        new_neighbors[x].add(y)
    for CC in CCs:
        for i in CC:
            new_neighbors[i] = new_neighbors[i]|CC[i]

    return [item.keys() for item in CCs], new_neighbors
