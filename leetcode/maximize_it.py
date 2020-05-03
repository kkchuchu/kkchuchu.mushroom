from itertools import product


def solve(K, M, L):
    max_ = 0
    max_arr = None
    for i in product(*L):
        tmp = sum([x**2 for x in i]) % M
        # print(tmp)
        if tmp > max_:
            max_ = tmp
            max_arr = i

    print(max_)
    print(max_arr)

def solve_v1(K, M, N):
    results = []
    max_ = 0
    for i in map(lambda x: sum(i**2 for i in x)%M, product(*N)):
        results.append(i)
        if i > max_:
            max_ = i
    print(max_)

solve_v1(6, 767, [[2, 488512261, 423332742],
               [2, 625040505, 443232774],
               [1, 4553600],
               [4, 92134264, 617699202, 124100179, 337650738],
               [2, 778493847, 932097163],
               [5, 489894997, 496724555, 693361712, 935903331, 518538304]])
solve(3, 1000, [[2, 5, 4], [3, 7, 8, 9], [5, 5, 7, 8, 9, 10]])
