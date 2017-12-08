# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def sumNumbers(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        self.sum = 0
        self.dfs(root, "")
        return self.sum

    def dfs(self, parent, s):
        # print parent.val, s
        for child in (parent.left, parent.right):
            if child is not None:
                self.dfs(child, s + str(parent.val))
        if parent.left is None and parent.right is None:
            self.sum = self.sum + int(s + str(parent.val))


root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)

print Solution().sumNumbers(root)
