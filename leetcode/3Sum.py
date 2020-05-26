from itertools import permutations, combinations


class Solution:
    def threeSum(self, nums):
        nums.sort()
        l = len(nums)
        result = set([])
        
        i = 0
        while i < l-2:
            j, k = i+1, l-1
            if nums[i] > 0:
                i += 1
                break
            while j < k < l:
                if nums[i] + nums[j] > 0:
                    break
                else:
                    j += 1
                    
            
        return result

                    
r = Solution().threeSum([-5,1,-10,2,-7,-13,-3,-8,2,-15,9,-3,-15,13,-6,-10,5,6,11,1,13,-12,14,6,11,4,13,-14,0,11,1,10,-11,6,-11,-10,8,2,-3,-13,-6,-9,-9,-6,11,-8,-9,1,13,9,9,3,13,0,-6,1,-10,-15,3,5,3,11,-8,0,2,-11,5,-13,6,9,-11,7,8,-13,8,4,-6,14,13,-15,1,7,-5,-1,-7,5,7,-2,-3,-13,10,7,13,9,-8,-8,13,12,-6,4,7,-10,-12,-8,-8,11,11,-6,3,9,-14,-11,2,-4,-5,10,8,-13,-7,12,-10,10])
print(r)