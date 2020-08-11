import LazyIter.utils as utils



def count_iterate_optimized(neighbors, source, dp, parents, hidden_CC, children_CCs, descendants_CCs, undirected_graph, verbose=False):
    if verbose:
        print("SS============================")
        print(neighbors, "\nsource: ", source, "\nparents: ", parents, "\nhidden_CC: ", hidden_CC, "\nchildren_CCs: ", children_CCs, "\ndescendants_CCs: ", descendants_CCs)
    children = neighbors[source]-parents

    sum_res = 0
    mult_res = 1
    for ccmp in children_CCs:
        k = LazyCount({i: ccmp & undirected_graph[i] for i in ccmp}, dp, verbose=verbose)
        mult_res *= k

    for ccmp in descendants_CCs:
        k = LazyCount({i: ccmp & undirected_graph[i] for i in ccmp}, dp, verbose=verbose)
        mult_res *= k

    g_graph = parents.union(hidden_CC)
    k = LazyCount({i: g_graph & undirected_graph[i] for i in g_graph}, dp, verbose=verbose)
    mult_res *= k

    sum_res += mult_res

    for c in children:
        if len(parents) == 0 or c > max(parents) and parents.issubset(undirected_graph[c]):
            tmp = [set(j.keys()) for j in (utils.separate_graph({i: neighbors[i] & children for i in children}))]

            c_comp = {}

            for cc in tmp:
                if c in cc:
                    c_comp = cc
            tmp.remove(c_comp)
            # print(c_comp," :/ ")
            # print({i: neighbors[i]&c_comp for i in c_comp})

            new_children_CCs, new_neighbors = utils.set_root_optimized(c, {i: neighbors[i]&c_comp for i in c_comp})
            new_children_CCs = [set(i) for i in new_children_CCs]
            new_children_CCs.extend(tmp)
            mult_res = 1
            cp = {i: neighbors[i].copy() for i in neighbors}
            for node in cp[c]:
                if c in cp[node]:
                    cp[node].remove(c)

            cp[source].remove(c)
            cp[c].add(source)
            reachable = utils.bfs_optimized(cp, source)

            new_desc_ccs = []
            new_hidden_CC = hidden_CC.copy()
            for cc in descendants_CCs:
                if cc.issubset(reachable):
                    new_desc_ccs.append(cc.copy())
                else:
                    new_hidden_CC = new_hidden_CC.union(cc)

            for i in new_hidden_CC:
                for j in cp[i]:
                    cp[j].add(i)

            new_parents = parents.copy()
            new_parents.add(c)
            k = count_iterate_optimized(cp, source, dp, new_parents, new_hidden_CC, new_children_CCs, new_desc_ccs, undirected_graph, verbose=verbose)
            sum_res += k

    return sum_res



def LazyCount(neighbors, dp={}, verbose=False):

    if verbose:
        print("Count on: ", neighbors.keys(),"                   ", neighbors)

    num_of_edges = sum([len(neighbors[i]) for i in neighbors]) / 2

    all_nodes = neighbors.keys()
    p = len(all_nodes)

    if p <= 1:
        return 1
    elif num_of_edges == p - 1:
        return (p)
    elif num_of_edges == p:
        return (2 * p)
    elif num_of_edges == p * (p - 1) / 2 - 1:
        return (2 * utils.fact[p - 1] - utils.fact[p - 2])
    elif num_of_edges == p * (p - 1) / 2:
        return (utils.fact[p])
    elif num_of_edges == p * (p - 1) / 2 - 2:
        return ((p * p - p - 4) * utils.fact[p - 3])

    ind = hash(str(neighbors.keys()))
    # if p > 5:
    if ind in dp:
        return dp[ind]


    tmp = list(all_nodes)
    best_node = tmp[0]
    for node in all_nodes:
        if len(neighbors[node]) < len(neighbors[best_node]):
            # print(len(neighbors[node]), len(neighbors[best_node]))
            best_node = node
    # if 6 in neighbors.keys():
    #     best_node = 6
    CCs, new_neighbors = utils.set_root_optimized(best_node, neighbors)
    for i in range(len(CCs)):
        CCs[i] = set(CCs[i])
    children_CCs = [neighbors[best_node]]

    descandant_CCs =  []
    for cc in CCs:
        if not cc == children_CCs[0]:
            descandant_CCs.append(cc)

    num = count_iterate_optimized(new_neighbors, best_node, dp, set(), set(), children_CCs, descandant_CCs, neighbors, verbose=verbose)

    # if p > 5:
    dp[ind] = num

    return num
