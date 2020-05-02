### Permutation
# from itertools import permutations
# algo for itertools.permutations: https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order

def toString(List): 
    return ''.join(List) 
  
# Function to print permutations of string 
# This function takes three parameters: 
# 1. String 
# 2. Starting index of the string 
# 3. Ending index of the string. 
def permute(a, l, r): 
    print(a, l, r)
    if l==r: 
        print toString(a) 
    else: 
        for i in xrange(l,r+1): 
            a[l], a[i] = a[i], a[l] 
            print("for 1st", a, i, l)
            permute(a, l+1, r) 
            a[l], a[i] = a[i], a[l] # backtrack 
            print("for 2ed", a, i, l)


# Driver program to test the above function 
string = "ABC"
n = len(string) 
a = list(string) 
permute(a, 0, n-1) 


### product


def product(pool, r=None):
    #result = [[]]
    #for i in range(r):
    #    result = [x+[y] for x in result for y in pool]
    result = [a for a in pool]
    for i in range(r-1):
        tmp = []
        for x in result:
            for a in pool:
                tmp.append(x+a) # change to yield
        result = tmp
            
        
    print(result, len(result))

product('ABC', r=3)


def c_product(*args, r=None):
    result = [[x] for x in args[0]]
    for arg in args[1:]:
        tmp = []
        for x in result:
            for y in arg:
                tmp.append(x+[y])
        result = tmp
        
    print(result, len(result))

c_product('ABC', "DE", "FG")


def permutation(pool, r=None):
    result = product("ABC", r=r)
    p_result = []
    for x in result:
        if len(list(set(x))) == r:
            p_result.append(x)
    print(p_result, len(p_result))
    
permutation("ABC", r=2)
