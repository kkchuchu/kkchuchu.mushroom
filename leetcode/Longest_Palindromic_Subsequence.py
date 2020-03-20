class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        text1 = s
        text2 = s[::-1]
        result = [[0] * (len(text2) + 1)]
        for i in range(1, len(text1) + 1):
            c1 = text1[i-1]
            tmp  = [0]
            for j in range(1, len(text2) + 1):
                c2 = text2[j-1]
                if c1 == c2:
                    tmp.append(result[i-1][j-1] + 1)
                else:
                    a = max(tmp[j-1], result[i-1][j])
                    tmp.append(a)
            result.append(tmp)

        # print(result)
        return result[-1][-1]
