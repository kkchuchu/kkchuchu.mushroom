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
        return self.create_new_tree(root)

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

    def create_new_tree(self, old_root):
        new_root = TreeNode(old_root.val)
        self.update_greater_sum(new_root, old_root, 0)
        return new_root

    def inorder_traversal(self, node, upper_right):
        if node.right:
            self.inorder_traversal(node.right, 0)
        if node.left:
            self.inorder_traversal(node.left, node.val + node.right_sum + node.left_sum)

    def update_greater_sum(self, new_node, node, upper_right):
        if node.right:
            new_node.right = TreeNode(node.right.val)
            self.update_greater_sum(new_node.right, node.right, 0) # this line has problem, cant find the upper sum from parent
            assert 1 == 2

            down_right_sum = node.right.right_sum + node.right.val + node.right.left_sum
        else:
            down_right_sum = 0
        new_node.val = node.val + down_right_sum + upper_right
        if node.left:
            new_node.left = TreeNode(node.left.val)
            self.update_greater_sum(new_node.left, node.left, new_node.val)


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

    r = util.bfs_bst(root)
    print(r)

    sol = Solution()
    new_root = sol.bstToGst(root)
    print(util.bfs_bst(new_root))
