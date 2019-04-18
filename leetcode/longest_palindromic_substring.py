class Solution(object):
    def longestPalindrome(self, S):
        """
        :type s: str
        :rtype: str
        """
        n = len(S)
        dp = [[] for i in range(n)]
        longest_len = -1
        longest_pair = (0, 0)
        for i, s_n_i in enumerate(S[::-1]):
            row = n-i-1
            for j, s_j in enumerate(S):
                if row == j:
                    dp[row].append(True)
                elif row < j:
                    dp[row].append((S[row] == S[j] and dp[row+1][j-1]))
                else:
                    dp[row].append(True)

                if dp[row][-1] and len(dp[row]) - row > longest_len:
                    longest_len = len(dp[row]) - row
                    longest_pair = (row, len(dp[row]))
        return S[longest_pair[0]: longest_pair[1]]
assert Solution().longestPalindrome("cbbd") == "bb"
s = Solution().longestPalindrome("babad")
print s
assert s == "bab"
