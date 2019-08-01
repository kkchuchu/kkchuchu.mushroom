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
        node.right_sum, node.left_sum = 0, 0
        if node.right:
            self.go_right_first(node.right, 0)
        if node.left:
            self.go_right_first(node.left, node.val)
        self.update_value(node, right_parent_value)

    def update_value(self, node, right_parent_value):
        if node.right:
            child = node.right
            node.right_sum = child.val + child.right_sum + child.left_sum
        if node.left:
            child = node.left
            node.left_sum = child.val + child.right_sum + child.left_sum


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
    from ktool import util

    sol = Solution()
    root = sol.bstToGst(root)

    r = []
    util.inorder_traversal(root, lambda x: x.val, r)
    print(r)
    r = []
    util.inorder_traversal(root, lambda x: x.right_sum, r)
    print(r)
    r = []
    util.inorder_traversal(root, lambda x: x.left_sum, r)
    print(r)
