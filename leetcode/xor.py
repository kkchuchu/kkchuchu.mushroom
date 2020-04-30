from functools import reduce
def solution(M, N):
    if N+1 - M <= 4:
        return reduce(lambda x, y: x^y, range(M, N+1))
    else:
        tmp = []
        for i in range(M, (int(M/4) + 1)*4):
            tmp.append(i)
        
        for i in range(N, int((N - tmp[-1]) / 4) * 4 + tmp[-1], -1):
            tmp.append(i)
        return reduce(lambda x, y: x^y, tmp)
    
def check(M, N):
    print("check", M, N, reduce(lambda x, y: x^y, range(M, N+1)))

print(solution(5, 8)) #12
print(solution(5, 5)) # 5
print(solution(5, 12)) # 8
print(solution(5, 12000)) # 8
print(solution(5, 12003)) # 8
print(solution(6, 13))
check(5, 12)
check(5, 12000)
check(6, 13)
check(5, 12003)