import math

class Solution(object):
    def getMoneyAmount(self, n):
        """
        :type n: int
        :rtype: int
        """
        self.db = [[0 for i in range(n+1)] for j in range(n+1)]
        self.r(n)
        return self.db[1][n]
        
    def r(self, n):
        for j in range(1, n+1):
            for i in range(j-1, 0, -1):
                if j-i == 1:
                    self.db[i][j] = i
                else:
                    self.db[i][j] = min([max(mid + self.db[i][mid-1], mid + self.db[mid+1][j]) for mid in range(i, j)])


if __name__ == '__main__':
    s = Solution()
    # assert s.getMoneyAmount(0) == 0
    # assert s.getMoneyAmount(1) == 0
    # assert s.getMoneyAmount(2) == 1
    # assert s.getMoneyAmount(3) == 2
    # assert s.getMoneyAmount(4) == 4
    assert s.getMoneyAmount(5) == 6
    assert s.getMoneyAmount(6) == 8
    assert s.getMoneyAmount(9) == 14
