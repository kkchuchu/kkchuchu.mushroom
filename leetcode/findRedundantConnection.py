'''
https://leetcode.com/problems/redundant-connection/description/
'''

class Solution(object):
    def findRedundantConnection(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        if len(edges) is 0:
            return []
        start = edges[0][0]
        visited = {tuple(edge): False for edge in edges}
        
        return self.is_circled(1)


    def is_circled(self, start):
        visited, stack = [], [start]
        while stack:
            begin = stack.pop()
            neighbors = []
            for edge in self.edges:
                if begin in edge:
                    neighbors.append(list(set(edge) - set([begin])))
                    visited.append(begin)
            stack = stack + self.edges[begin]


print Solution().findRedundantConnection([[1, 2], [1, 3], [2, 3]])
print Solution().findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]])
