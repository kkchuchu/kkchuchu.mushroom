class Solution:
    def palindromePairs(self, words: list):
        l = len(words)
        ans = []
        for i in range(l):
            for j in range(l):
                if i != j and self._is_palindrome(words[i] + words[j]):
                    ans.append([i, j])
        
        # print(ans)
        return ans
    
    def _is_palindrome(self, s):
        i, j = 0, len(s)-1
        while i < j:
            if s[i] != s[j]:
                return False
            else:
                i += 1
                j -= 1
        return True
    
    
sol = Solution()

assert sol.palindromePairs(["abcd","dcba","lls","s","sssll"]) == [[0,1],[1,0],[3,2],[2,4]]
assert sol.palindromePairs(["bat","tab","cat"]) == [[0,1],[1,0]] 