# This is essentially going to be a Python translation of the algorithm
# found at https://kaygun.github.io/clean/2020-12-18-counting_graphs_with_a_prescribed_degree_sequence.html
# They did it in Common Lisp

from itertools import combinations
from functools import cache

# caching the function and using tuples gives us fast memoization for free
@cache
def count_graphs(deg_seq: tuple[int]) -> int:
    n = len(deg_seq)
    if n == 0:
        return 1
    elif n == 2 and deg_seq == (1,1):
        return 1
    elif n < 3:
        return 0
    elif sum(deg_seq) % 2 == 1:
        return 0
    
    total = 0
    for indices in combinations(range(n-1), deg_seq[0]):
        rest = list(deg_seq[1:])
        for idx in indices:
            rest[idx] -= 1
        new_seq = tuple(sorted((x for x in rest if x != 0), reverse=True))
        total += count_graphs(new_seq)
    return total
        
        

# Maybe using algorithm from https://arxiv.org/pdf/0905.4892
# This is ultimately a way of optimizing the above method by excluding subtrees
'''
Given:
    n = |V|
    sequence = (d1, d2, ..., dn)
    d1 >= d2 >= ... >= dn >= 1
1.) Create rightmost adjacency set Ar(1) for node 1
    a.) Connect node 1 to n
    b.) k := n - 1
    c.) Connect 1 to k. Run constrained graphicality test
        Remove connection if fails
    d.) k--
    e.) If 1 has connections left to make, back to (c)
2.) Create set of all adjacency sets of node 1 that are colexicographically 
    smaller than Ar(1) and preserve graphicality:
    A(d) := {A subset V | A <CL Ar(1) and d-A graphical}
    a.) <CL is lexicographic order from right to left
    b.) graphicality implied by <
3.) Add graph count of d-A for all A in A(d)
'''

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