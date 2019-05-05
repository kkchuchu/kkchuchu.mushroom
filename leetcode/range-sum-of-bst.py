# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def rangeSumBST(self, root, L, R):
        """
        :type root: TreeNode
        :type L: int
        :type R: int
        :rtype: int
        """
        stack = [root]
        sum_ = 0

        while len(stack) > 0:
            node = stack.pop()
            if node.left is not None and node.val >= L:
                stack.append(node.left)
            if node.right is not None and node.val <= R:
                stack.append(node.right)

            if L <= node.val <= R:
                sum_ += node.val

        return sum_
