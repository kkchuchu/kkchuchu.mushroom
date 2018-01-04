class Solution(object):
    def longestIncreasingPath(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: int
        """
        self.max_len_path = 0
        self.visited = []
        x = len(matrix[0])
        y = len(matrix)
        self.visited.append([{'val':0, 'visited': True, 'x': i, 'y': 0} for i in range(x+2)])
        for j in range(y):
            temp_x = [{'visited': True, 'val': 0, 'x': 0, 'y': j+1}]
            for i in range(x):
                temp_x.append({'visited':False, 'val': matrix[j][i], 'x': i+1, 'y': j+1})
            temp_x.append({'visited': True, 'val': 0, 'x': x+1, 'y': j+1})
            self.visited.append(temp_x)
        self.visited.append([{'val':0, 'visited': True, 'x': i, 'y': y+1} for i in range(x+2)])
        # return self.visited

        for j in self.visited[1:]:
            for i in j[1:]:
                self.dfs(i, 0, 0)
        return self.max_len_path
        
    def dfs(self, cursor, len_path, last_value):
        x = cursor['x']
        y = cursor['y']
        current_val = cursor['val']
        cursor['visited'] = True

        len_path += 1
        if len_path > self.max_len_path:
            self.max_len_path = len_path

        go_right, pt = self.go_somewhere((x, y), (+1, 0), last_value)
        if go_right:
            self.dfs(pt, len_path, current_val)
        go_left, pt = self.go_somewhere((x, y), (-1, 0), last_value)
        if go_left:
            self.dfs(pt, len_path, current_val)
        go_down, pt = self.go_somewhere((x, y), (0, +1), last_value)
        if go_down:
            self.dfs(pt, len_path, current_val)
        go_up, pt = self.go_somewhere((x, y), (0, -1), last_value)
        if go_up:
            self.dfs(pt, len_path, current_val)
        

    def go_somewhere(self, cursor, offset, last_value):
        x = cursor[0] + offset[0]
        y = cursor[1] + offset[1]
        if x >= len(self.visited):
            return False, 0
        if y >= len(self.visited):
            return False, 0
        if not self.visited[x][y]['visited'] and self.visited[x][y]['val'] > last_value:
            return (True, self.visited[x][y])
        return (False, self.visited[x][y])




nums = [
    [3,4,5],
    [3,2,6],
    [2,2,1],
]

print Solution().longestIncreasingPath(nums)

nums = [
    [0],
    [1],
    [5],
    [5]
]

print Solution().longestIncreasingPath(nums)
