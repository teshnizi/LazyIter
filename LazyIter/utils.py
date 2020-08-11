import queue


# def get_all_subsets(st):
#     ret = []
#     for i in range(len(st) + 1):
#         lst = list(itertools.combinations(st, i))
#         for item in lst:
#             ret.append(list(item))
#     return ret


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

    # t = ttictoc.TicToc()
    # t.tic()

    added_edges = []
    q = queue.Queue()


    for i in neighbors[root]:
        if is_valid[i] and adj_mat[root][i] == 1 and adj_mat[i][root] == 1:
            added_edges.append((root, i))
            q.put((root, i))
            adj_mat[i][root] = 0
    # total_hash_time[4] += t.toc()
    """
    If the graph is not chordal, direction of the root's edges might be overwritten in the following while-loop! 
    """
    # t.tic()
    while not q.empty():
        s, e = q.get()
        for i in neighbors[e]:
            if is_valid[i] and adj_mat[e][i] == 1 and adj_mat[i][e] == 1 and adj_mat[s][i] == 0 and adj_mat[i][s] == 0:
                added_edges.append((e, i))
                q.put((e, i))
                adj_mat[i][e] = 0

    # total_hash_time[5] += t.toc()
    return added_edges




def encode(lst):
    w = 1
    sm = 0
    for i in lst:
        if i:
            sm += w
        w *= 2
    return sm




def find_chain_components(adj_mat, neigbors, is_valid):
    n = len(adj_mat)
    component_id = [-1] * n
    current_id = 0
    for i in range(n):
        if is_valid[i]:
            if component_id[i] == -1:
                q = queue.Queue()
                q.put(i)
                while not q.empty():
                    node = q.get()
                    component_id[node] = current_id
                    for v in neigbors[node]:
                        if component_id[v] == -1 and is_valid[v] and adj_mat[v][node] == 1 and adj_mat[node][v] == 1:
                            # print(node+1, v+1, component_id[v])
                            q.put(v)
                current_id += 1

    return [[num for num in list(range(n)) if component_id[num] == id] for id in range(current_id)]
    # for id in range(current_id):
    #     print([num+1 for num in list(range(n)) if component_id[num] == id])



fact = [1] * 5000
for i in range(1,5000):
    fact[i] = fact[i-1] * i
