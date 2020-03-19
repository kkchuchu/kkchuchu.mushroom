class Solution:
    def lengthOfLIS(self, nums):
        if len(nums) is 0:
            return 0

        envelops = nums
        result = [1]
        for i in range(1, len(envelops)):
            ds = envelops[i]
            tmp = []
            for j in range(0, i):
                sds = envelops[j]
                if sds < ds:
                    tmp.append(result[j])

            if len(tmp) == 0:
                result.append(1)
            else:
                result.append(max(tmp) + 1)

            # print(result, tmp)

        # print(envelops, result)
        return max(result)


assert 4 == Solution().lengthOfLIS([10,9,2,5,3,7,101,18])