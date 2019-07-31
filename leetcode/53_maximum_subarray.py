class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        tmp = [0]
        min_, max_ = 0, 0
        for i, num in enumerate(nums):
            current = tmp[-1] + num
            tmp.append(current)

        largest_sum = tmp[1]
        for i, s_i in enumerate(tmp):
            for j, s_j in enumerate(tmp[1+i:]):
                if s_j - s_i >= largest_sum:
                    largest_sum = s_j - s_i
        # print(tmp)
        return largest_sum



s = Solution()
print(s.maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))
print(s.maxSubArray([-1]))
print(s.maxSubArray([-2, 1]))
print(s.maxSubArray([1, 2]))
