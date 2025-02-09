# This is essentially going to be a Python translation of the algorithm
# found at https://kaygun.github.io/clean/2020-12-18-counting_graphs_with_a_prescribed_degree_sequence.html
# They did it in Common Lisp

from itertools import combinations
from functools import cache

# caching the function and using tuples gives us fast memoization for free
@cache
def count_graphs(deg_seq: tuple[int]) -> int:
    """
    Count number of simple graphs with given degree sequence

    This is a brute-force recursive approach, but is fast for small graphs

    :param tuple[int] deg_seq: a non-increasing sequence of integers, corresponding to the degrees of the vertices of a graph
    """
    n = len(deg_seq)
    if n == 0:
        # the empty graph counts, and the logic depends on this base case
        return 1
    elif n == 2 and deg_seq == (1,1):
        # we can't reduce this base case through our normal recursive step
        return 1
    elif n < 3:
        # degree sequences of length 2 or smaller other than (,) and (1,1) are
        # not realizable as a simple graph
        return 0
    elif sum(deg_seq) % 2 == 1:
        # sum(degrees) == 2*edges, so must be even to be realizable
        return 0
    
    total = 0
    # every possible way of connecting the highest-degree node
    for indices in combinations(range(n-1), deg_seq[0]):
        rest = list(deg_seq[1:])
        for idx in indices:
            rest[idx] -= 1
        # the degree sequence if we remove the highest-degree node
        new_seq = tuple(sorted((x for x in rest if x != 0), reverse=True))
        total += count_graphs(new_seq)
    return total
        
if __name__ == "__main__":
    # every deg_seq is of the form a*(4,) + b*(3,) + c*(2,)
    # a+b+c=13
    # b >= 7
    types = {}
    total = 0
    for fours in range(14):
        for threes in range(7,14-fours):
            twos = 13 - fours - threes
            count = count_graphs(fours*(4,) + threes*(3,) + twos*(2,))
            label = (fours,threes,twos)
            print(f"{label}: {count}")
            total += count
            print(f"Total: {total}")
            print()
            types[label] = count