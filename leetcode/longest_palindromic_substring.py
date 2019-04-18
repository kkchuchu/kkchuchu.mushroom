class Solution(object):
    def longestPalindrome(self, S):
        """
        :type s: str
        :rtype: str
        """
        dp = []
        longest_len = -1
        longest_pair = (0, 0)
        for i, s_i in enumerate(S):
            dp_i = []
            dp.append(dp_i)
            for j, s_j in enumerate(S):
                if i == j:
                    dp_i.append(True)
                elif i < j:
                    dp[i][j] = (S[i] == S[j+1] and S[i+1][j])
                else:
                    dp_i.append(0)
        print dp

    def is_pal(self, S):
        if len(S) == 0:
            return True
        elif S[0] == S[-1]:
            return self.is_pal(S[1:-2])
        else:
            return False

assert Solution().longestPalindrome("babad") == "bab"
