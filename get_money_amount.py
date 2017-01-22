import math

class Solution(object):
    def getMoneyAmount(self, n):
        """
        :type n: int
        :rtype: int
        """
        self.db = [0 for i in range(n+1)]
        self.r(n)
        return self.db[n]
        
    def r(self, n):
        for i in range(2, n+1):
            if i == 2:
                self.db[i] = 1
            elif i == 3:
                self.db[3] = 2
            else:
                self.db[i] = min([self.db[i-2] + i-1, max(i-2 + i-1, self.db[i-3] + i-2), max(self.db[i-4] + i-3, i-3 + i-1)])


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
