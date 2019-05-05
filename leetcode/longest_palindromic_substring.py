class Solution(object):
    def longestPalindrome(self, S):
        """
        :type s: str
        :rtype: str
        """
        n = len(S)
        dp = []
        longest_len = -1
        longest_pair = (0, 0)
        for i, s_n_i in enumerate(S[::-1]):
            dp_n_i = []
            row = n-i-1
            for j, s_j in enumerate(S):
                if len(dp) <= n:
                    dp.append([])
                if row == j:
                    dp_n_i.append(True)
                elif row < j:
                    dp_n_i.append((S[row] == S[j] and dp[row+1][j-1]))
                else:
                    dp_n_i.append(True)

                if dp_n_i[-1] and len(dp_n_i) - row > longest_len:
                    longest_len = len(dp_n_i) - row
                    longest_pair = (row, len(dp_n_i))

        print(dp)
        return S[longest_pair[0]: longest_pair[1]]
assert Solution().longestPalindrome("cbbd") == "bb"
assert Solution().longestPalindrome("babad") == "bab"
