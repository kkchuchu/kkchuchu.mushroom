import os

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def binaryTreePaths(self, root):
        self.result = []
        self.path = ""
        self.visit(root)
        return self.result

    def visit(self, node):
        if self.path == "":
            self.path = str(node.val)
        else:
            self.path += "->" + str(node.val)
        if node.left is None and node.right is None:
            self.result.append(self.path)
            self.path = ""
            return None
        if node.left is not None:
            self.visit(node.left)
        if node.right is not None:
            self.visit(node.right)
        
if __name__ == '__main__':
    s = Solution()
    t1 = TreeNode(1)
    t1.left = TreeNode(2)
    t1.right = TreeNode(3)
    t1.left.right = TreeNode(5)
    result = s.binaryTreePaths(t1)
    print(result)
    assert ["1->2->5", "1->3"] == result
