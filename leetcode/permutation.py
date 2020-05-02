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

