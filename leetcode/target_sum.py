from collections import defaultdict

"""
leet code: #494
You are given a list of non-negative integers, a1, a2, ..., an, and a target, S. Now you have 2 symbols + and -. For each integer, you should choose one from + and - as its new symbol.

Find out how many ways to assign symbols to make sum of integers equal to target S.
"""


class Solution(object):
    def findTargetSumWays(self, nums, S):
        """
        :type nums: List[int]
        :type S: int
        :rtype: int
        """
        
        dp = {0: 1}
        for num in nums:
            temp_dp = defaultdict(int)
            for sum, counter in dp.items():
                temp_dp[sum + num] += counter
                temp_dp[sum - num] += counter
            dp = temp_dp
            
        return dp[S]
        
        """
        if len(nums) == 0:
            if S == 0:
                return 1
            else:
                return 0
        return self.findTargetSumWays(nums[1:], S+nums[0]) + self.findTargetSumWays(nums[1:], S-nums[0])
        """
