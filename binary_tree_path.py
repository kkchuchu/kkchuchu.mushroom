import os
"""
https://leetcode.com/problems/binary-tree-paths/
"""
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    """
    From bottom to root, chain node to path.
    """
    def binaryTreePaths(self, root):
        if not root:
            return []
        return [str(root.val) + "->" + path
                for kid in (root.left, root.right) if kid
                for path in self.binaryTreePaths(kid)] or [str(root.val)]
        
if __name__ == '__main__':
    s = Solution()
    t1 = TreeNode(1)
    t1.left = TreeNode(2)
    t1.right = TreeNode(3)
    t1.left.right = TreeNode(5)
    result = s.binaryTreePaths(t1)
    print(result)
    assert ["1->2->5", "1->3"] == result
