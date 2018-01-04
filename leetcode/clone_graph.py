# Definition for a undirected graph node
class UndirectedGraphNode:
    def __init__(self, x):
        self.label = x
        self.neighbors = []


class Solution:
    # @param node, a undirected graph node
    # @return a undirected graph node
    def cloneGraph(self, node):
        visited, stack = [], [node]
        last = None
        while stack:
            cursor = stack.pop()
            last = self._copy(cursor)
            visited.append(cursor)
            for child in cursor.neighbors:
                if child not in visited:
                    stack.append(child)
                last.neighbor.append(self._copy(child))

        return last

    def _copy(self, node):
        r = UndirectedGraphNode(node.label)
        r.left = node.left
        r.right = node.right
        return r


Undire
