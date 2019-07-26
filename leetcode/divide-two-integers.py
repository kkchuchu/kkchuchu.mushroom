class Solution(object):
    def divide(self, dividend, divisor):
        """
        :type dividend: int
        :type divisor: int
        :rtype: int
        """
        m = 1
        if dividend * divisor < 0:
            m = -1
        if dividend < 0:
            dividend = -1 *dividend
        if divisor < 0:
            divisor = -1 * divisor
        c = 0
        while True:
            print(dividend, divisor)
            if dividend < divisor or dividend is 0:
                break
            else:
                c += 1
                dividend = dividend - divisor
        return c * m



s = Solution()
assert -1==s.divide(-1, 1)
assert 2147483648==s.divide(-2147483648, -1)
