# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def bstToGst(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """
        self.go_right_first(root, 0)
        return root

    def go_right_first(self, node, right_parent_value):
        if node.right:
            self.go_right_first(node.right, right_parent_value)
        self.update_value(node, right_parent_value)
        if node.left:
            self.go_right_first(node.left, node.val)

    def update_value(self, node, right_parent_value):
        node.val = right_parent_value + node.val
        


if __name__ == '__main__':
    root = TreeNode(4)
    root.left = TreeNode(1)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(2)
    root.left.right.right = TreeNode(3)
    root.right = TreeNode(6)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(7)
    root.right.right.right = TreeNode(8)
    sol = Solution()
    root = sol.bstToGst(root)
    print root.val
