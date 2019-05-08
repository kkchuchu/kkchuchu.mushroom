
a = "ABC"
used = set([])
print(used)

solution = ["" for i in range(len(a))]
def backtrack(a, dimension, used):
    if dimension == len(a):
        print solution
        return

    for i in a:
        if i not in used:
            solution[dimension] = i
            used = used | set(i)
            backtrack(a, dimension+1, used)
            used = used - set(i)
        else:
            continue


backtrack(a, 0, used)
