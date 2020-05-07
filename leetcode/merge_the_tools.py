def merge_the_tools(string, k):
    for i in range(0, len(string), k):
        tmp = set([])
        p_list = []
        for j in string[i:i+k]:
            if j not in tmp:
                tmp.add(j)
                p_list.append(j)
              
        
        print("".join(p_list))
    # your code goes here

if __name__ == '__main__':
    merge_the_tools("AABCAAADA", 3)