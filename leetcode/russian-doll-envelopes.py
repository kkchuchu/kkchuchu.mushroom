class Solution(object):
    def maxEnvelopes(self, envelops):
        l = len(envelops)
        if l == 0:
            return l
        envelops[0].append(1)
        ordered = [envelops[0]]
        for envelop in envelops[1:]:
            max_val = ordered[0][2]
            position = 0
            for i, o_envelop in enumerate(ordered):
                if envelop[0] > o_envelop[0] or envelop[1] > o_envelop[1]:
                    position += 1
                    if envelop[0] > o_envelop[0] and envelop[1] > o_envelop[1] \
                            and max_val <= o_envelop[2]:
                        max_val += 1
                else:
                    break

            envelop.append(max_val)
            ordered.insert(position, envelop)
            for o_envelop in ordered[position+1:]:
                if envelop[0] < o_envelop[0] and \
                        envelop[1] < o_envelop[1]:
                    o_envelop[2] = o_envelop[2] + 1
                print(o_envelop[2])
                if envelop[0] == o_envelop[0] and \
                        envelop[1] == o_envelop[1]:
                    break
        from pdb import set_trace; set_trace()

        return max(ordered, key=lambda x: x[2])[2]


if __name__ == '__main__':
    # assert 3 == Solution().maxEnvelopes([[5, 4], [6, 4], [6, 7], [2, 3]])
    # assert 1 == Solution().maxEnvelopes([[1,1], [1,1], [1,1]])
    # assert 3 == Solution().maxEnvelopes([[4,5],[6,7],[2,3]])
    # assert 4 == Solution().maxEnvelopes([[4,5],[4,6],[6,7],[2,3],[1,1]])
    # assert 4 == Solution().maxEnvelopes([[4,5],[4,6],[6,7],[2,3],[1,1],[1,1]])
    assert 3 == Solution().maxEnvelopes([[30,50],[12,2],[3,4],[12,15]])
