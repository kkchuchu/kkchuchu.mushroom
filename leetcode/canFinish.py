class Solution(object):
    def canFinish(self, numCourses, prerequisites):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :rtype: bool
        """
        self.ll2ll(numCourses, prerequisites)
        print self.edges
        visited = []
        for node in self.edges.keys():
            # handle unconnected graph
            if node not in visited:
                if self.is_cyclic(node, visited, []):
                    return True
            print "next round"
        return False


    def ll2ll(self, n, edges):
        self.edges = {i: [] for i in range(n)}
        for edge in edges:
            [end, start] = edge
            if start not in self.edges:
                self.edges[start] = []
            self.edges[start].append(end)

        
    def is_cyclic(self, start, visited, stack):
        # print "start", start, "visited", visited, "stack", stack
        stack.append(start)
        visited += [start]
        # print "start", start, "visited", visited, "stack", stack
        for neighbor in self.edges[start]: 
            print "start ", start, "neighbor", neighbor
            if neighbor in stack:
                return True
            if neighbor not in visited:
                if self.is_cyclic(neighbor, visited, stack):
                    return True
        stack.pop()

        return False


# Solution().canFinish(2, [[0,1]]) # no circle
print "====="
print Solution().canFinish(3, [[1,0],[2,0],[0,2]])
print "====="
# print Solution().canFinish(2, [[0,1], [1,0]]) # circle
print "====="
# print Solution().canFinish(1, []) # no circle
print "====="
# print Solution().canFinish(3, [[0, 1], [0, 2], [1, 2]])
print "====="
# Solution().canFinish(4, [[1,0],[2,0],[3,1],[3,2]])
print "====="
