class Solution:

    def countSubstrings(self, s: str) -> int:
        l = len(s)
        ans = [[(False, 0) for i in range(l+1)] for j in range(l+1)]
        end, max_l = 0, 0
        for i in range(l-1, -1, -1):
            for j in range(0, l):
                # print(i, j)
                if i == j:
                    ans[i][j] = (True, 1)
                    if 1 > max_l:
                        max_l = 1
                        end = j+1
                elif j > i:
                    if s[j] == s[i]:
                        if ans[i+1][j-1][0] or j - i == 1:
                            ans[i][j] = (True, 1)

                else:
                    continue

        #　print(ans, max_l, end, s[end-max_l:end])
        return sum([sum([x[0] for x in a]) for a in ans])


sol = Solution()
assert 6 == sol.countSubstrings("aaa")
assert 3 == sol.countSubstrings("abc")
assert 3 == sol.countSubstrings("aa")
