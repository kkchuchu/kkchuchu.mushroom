# Definition for a binary tree node.
# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def maxPathSum(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        self.max_ = root.val
        self.maxmp(root)
        return self.max_
        
    def maxmp(self, parent):
        if parent is None:
            return 0
        l = self.maxmp(parent.left)
        r = self.maxmp(parent.right)
        self.max_ = max(self.max_, l + r + parent.val)
        return max(max(l, r) + parent.val, 0)
        
root = TreeNode(1)
left = TreeNode(2)
right = TreeNode(3)

root.left, root.right = left, right

s = Solution()
s.maxPathSum(root)
print s.max_
