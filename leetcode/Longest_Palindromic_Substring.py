class Solution(object):

    def longestPalindrome(self, s):
        l = len(s)
        ans = [[(False, 0) for i in range(l+1)] for j in range(l+1)]
        end, max_l = 0, 0
        for i in range(l-1, -1, -1):
            for j in range(0, l):
                # print(i, j)
                if i == j:
                    ans[i][j] =  (True, 1)
                    if 1 > max_l:
                        max_l = 1
                        end = j+1
                elif j > i:
                    if s[j] == s[i]:
                        if ans[i+1][j-1][0] or j - i == 1:
                            tmp_max = len(s[i:j+1])
                            ans[i][j] = (True, tmp_max)
                            if tmp_max > max_l:
                                max_l = tmp_max
                                end = j+1
                            
                        
                else:
                    continue
        
        # print(ans, max_l, end, s[end-max_l:end])
        return s[end-max_l:end]
    
    def _is_palindrome(self, s):
        i, j = 0, len(s)-1
        ans = True
        if len(s) == 0:
            return False
        while i < j:
            if s[i] == s[j]:
                i += 1
                j -= 1
            else:
                ans = False
                break
        return ans


assert "bb" == Solution().longestPalindrome("cbbd")
assert Solution().longestPalindrome("babad") in [ "bab", "aba"]
assert Solution().longestPalindrome("abcda") == "a"
assert "bab" == Solution().longestPalindrome("bab")
assert "aa" == Solution().longestPalindrome("aacdefcaa")
assert "bb" == Solution().longestPalindrome("abcdbbfcba")
