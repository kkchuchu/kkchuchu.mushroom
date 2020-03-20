class Solution(object):

    def longestPalindrome(self, s):
        ans = 0
        ans_s = None
        l = len(s)
        for i in range(l):
            for j in range(i, l):
                # import pdb; pdb.set_trace()
                if self._is_palindrome(s[i:j+1]):
                    if len(s[i:j+1]) > ans:
                        ans = len(s[i:j+1])
                        ans_s = s[i:j+1]

        # print(ans, ans_s)
        return ans_s

    def _is_palindrome(self, s):
        i, j = 0, len(s)-1
        ans = True
        while i < j:
            if s[i] == s[j]:
                i += 1
                j -= 1
            else:
                ans = False
                break
        # print(s, ans)
        return ans


assert "bb" == Solution().longestPalindrome("cbbd")
assert "bab" == Solution().longestPalindrome("babad")
assert "bab" == Solution().longestPalindrome("bab")
