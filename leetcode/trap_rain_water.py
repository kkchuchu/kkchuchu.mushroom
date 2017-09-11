import os


class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        water_pool = 0
        right_wall, left_wall = 0, 0
        for i, horizan in enumerate(height):
            if i > 0:
                left_wall = max(left_wall, height[i-1])
            if horizan >= right_wall:
                right_wall = max(height[i+1:] or [0])
            m = min(left_wall, right_wall)
            print left_wall, m - horizan, right_wall
            if m - horizan > 0:
                water_pool += m - horizan
        return water_pool


if __name__ == '__main__':
    s = Solution()
    assert s.trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
