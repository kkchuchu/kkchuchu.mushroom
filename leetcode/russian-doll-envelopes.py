class Solution(object):
    def maxEnvelopes(self, envelops):
        if len(envelops) is 0:
            return 0
        
        envelops = sorted(envelops)
        result = [1]
        # print(envelops)
        for i in range(1, len(envelops)):
            ds = envelops[i]
            tmp = []
            for j in range(0, i):
                sds = envelops[j]
                if sds[0] < ds[0] and sds[1] < ds[1]:
                    tmp.append(result[j])
            
            if len(tmp) == 0:
                result.append(1)
            else:
                result.append(max(tmp) + 1)
                
            # print(result, tmp)
                
            
        # print(max(result))
        return max(result)
            


if __name__ == '__main__':
    assert 3 == Solution().maxEnvelopes([[1,3],[3,5],[6,7],[6,8],[8,4],[9,5]])
    assert 3 == Solution().maxEnvelopes([[5, 4], [6, 4], [6, 7], [2, 3]])
    assert 1 == Solution().maxEnvelopes([[1,1], [1,1], [1,1]])
    assert 3 == Solution().maxEnvelopes([[4,5],[6,7],[2,3]])
    assert 4 == Solution().maxEnvelopes([[4,5],[4,6],[6,7],[2,3],[1,1]])
    assert 4 == Solution().maxEnvelopes([[4,5],[4,6],[6,7],[2,3],[1,1],[1,1]])
    assert 3 == Solution().maxEnvelopes([[30,50],[12,2],[3,4],[12,15]])
