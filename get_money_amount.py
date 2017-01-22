import math

class Solution(object):
    def getMoneyAmount(self, n):
        """
        :type n: int
        :rtype: int
        """
        dp = [0 for i in range(n)]
        return self.r(math.ceil(float(n)/2))
        
    def r(self, n):
        if n == 1:
            return 0
        if len(n) == 2:
            return 
        return n + self.r(math.ceil(float(n)/2))


if __name__ == '__main__':
    s = Solution()
    assert s.getMoneyAmount(0) == 0
    assert s.getMoneyAmount(1) == 1
    assert s.getMoneyAmount(2) == 2
    assert s.getMoneyAmount(3) == 4
    assert s.getMoneyAmount(4) == 6
    assert s.getMoneyAmount(5) == 8
