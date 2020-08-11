from LazyIter.count import LazyCount

neighbors = {
        0: {3,1,2},
        1: {0,2},
        2: {1,3,0},
        3: {2,0}
        }

print(LazyCount(neighbors, verbose=True))
