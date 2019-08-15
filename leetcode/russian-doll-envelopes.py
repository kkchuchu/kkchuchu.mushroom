class Solution(object):
    def maxEnvelopes(self, envelops):
        l = len(envelops)
        if l == 0:
            return l
        envelops[0].append(1)
        tmp, index, stop = [envelops[0]], 0, False
        for envelop in envelops[1:]:
            for i, i_envelop in enumerate(tmp):
                if envelop[0] > i_envelop[0]:
                    continue
                elif envelop[1] > i_envelop[1]:
                    continue
                elif envelop[0] == i_envelop[0] and envelop[1] == i_envelop[1]:
                    break
                else:
                    if not stop:
                        index = i
                        stop = True
                    if envelop[0] < i_envelop[0] and \
                            envelop[1] < i_envelop[1]:
                        i_envelop[2] = i_envelop[2] + 1

            envelop.append(index)
            tmp.insert(index, envelop)
            print(tmp, envelop, index)

        return max(tmp, key=lambda x: x[2])[2]


if __name__ == '__main__':
    print(Solution().maxEnvelopes([[5, 4], [6, 4], [6, 7], [2, 3]]))
    print(Solution().maxEnvelopes([[1,1], [1,1], [1,1]]))
