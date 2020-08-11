
import LazyIter.utils as utils

def evaluate_iterate_optimized(neighbors, source, targets, dp, parents, hidden_CC, children_CCs, descendent_CCs, undirected_graph, verbose=False):

    children = neighbors[source]-parents

    case_score = 0

    for i in neighbors:
        for j in neighbors[i]:
            if not i in neighbors[j]:
                case_score += 1

    ss = [case_score]
    for ccmp in children_CCs:
        s = PLScore({i: ccmp & undirected_graph[i] for i in ccmp}, ccmp & targets, dp, verbose=verbose)
        ss.append((s, ccmp))
        case_score += s

    for ccmp in descendent_CCs:
        s = PLScore({i: ccmp & undirected_graph[i] for i in ccmp}, ccmp & targets, dp, verbose=verbose)
        ss.append(s)
        case_score += s

    g_graph = parents.union(hidden_CC)
    s = PLScore({i: g_graph & undirected_graph[i] for i in g_graph}, g_graph&targets, dp, verbose=verbose)
    ss.append(s)
    case_score += s

    min_score = case_score

    for c in children:
        if len(parents) == 0 or (c > max(parents) and parents.issubset(undirected_graph[c])):

            tmp = [set(j.keys()) for j in (utils.separate_graph({i: neighbors[i] & children for i in children}))]
            c_comp = {}
            for cc in tmp:
                if c in cc:
                    c_comp = cc
            tmp.remove(c_comp)

            new_children_CCs, new_neighbors = utils.set_root_optimized(c, {i: neighbors[i] & c_comp for i in c_comp})

            new_children_CCs = [set(i) for i in new_children_CCs]
            new_children_CCs.extend(tmp)
            cp = {i: neighbors[i].copy() for i in neighbors}

            for i in new_neighbors:
                for j in new_neighbors:
                    if j in cp[i] and (not j in new_neighbors[i]):
                        cp[i].remove(j)


            for node in cp[c]:
                if c in cp[node]:
                    cp[node].remove(c)

            cp[source].remove(c)
            cp[c].add(source)
            reachable = utils.bfs_optimized(cp, source)

            new_desc_ccs = []
            new_hidden_CC = hidden_CC.copy()

            for cc in descendent_CCs:
                # print("CC  ", cc)
                if c in cc:
                    cc.remove(c)
                if cc.issubset(reachable):
                    new_desc_ccs.append(cc.copy())
                else:
                    new_hidden_CC = new_hidden_CC.union(cc)


            new_parents = parents.copy()
            new_parents.add(c)

            g_graph = new_hidden_CC.union(new_parents)
            for i in g_graph:
                for j in cp[i]&g_graph:
                    cp[j].add(i)


            s = evaluate_iterate_optimized(cp, source, targets, dp, new_parents, new_hidden_CC, new_children_CCs, new_desc_ccs,
                                           undirected_graph, verbose=verbose)
            if s < min_score:
                min_score = s

    return min_score


def PLScore(neighbors, targets, dp={}, verbose=False):
    ind = hash(str(neighbors) + str(targets))
    if len(neighbors) <= 1 or len(targets) <= 0:
        return 0

    if ind in dp:
        return dp[ind]

    best_target = "NA"

    for tg in targets:
        if best_target == "NA":
            best_target = tg
        if len(neighbors[tg]) < len(neighbors[best_target]):
            best_target = tg


    CCs, new_neighbors = utils.set_root_optimized(best_target, neighbors)

    for i in range(len(CCs)):
        CCs[i] = set(CCs[i])
    children_CCs = [neighbors[best_target]]

    descandant_CCs = []
    for cc in CCs:
        if not cc == children_CCs[0]:
            descandant_CCs.append(cc)

    max_score = evaluate_iterate_optimized(new_neighbors, best_target, targets, dp, set(), set(), children_CCs, descandant_CCs, neighbors,
                                  verbose=verbose)

    if verbose:
        print("Score of target set ", targets, " on subgraph ", list(neighbors.keys()), "  is ", max_score)
    dp[ind] = max_score

    return dp[ind]
