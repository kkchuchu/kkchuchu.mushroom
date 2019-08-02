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

        # inorder traversal tree
        r = []
        self.inorder_traversal(root, r)
        print(r)
        new_root = TreeNode(root.val)
        self.create_tree(root, new_root, r)
        return new_root

    def inorder_traversal(self, node, r):
        if node is None:
            return 

        self.inorder_traversal(node.left, r)
        r.append(node.val)
        self.inorder_traversal(node.right, r)

    def create_tree(self, node, new_node, r):
        new_node.val = sum(r[r.index(node.val):])
        if node.left:
            new_node.left = TreeNode(sum(r[r.index(node.left.val):]))
            self.create_tree(node.left, new_node.left, r)
        if node.right:
            new_node.right = TreeNode(sum(r[r.index(node.right.val):]))
            self.create_tree(node.right, new_node.right, r)


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
    new_root = sol.bstToGst(root)
    print(util.bfs_bst(new_root))
