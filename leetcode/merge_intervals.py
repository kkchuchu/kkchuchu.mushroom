class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """
        if len(intervals) == 0:
            return intervals
        intervals = sorted(intervals, key=lambda x: x[0])

        merged_intervals = [intervals[0]]
        for i in intervals[1:]:
            start, end = i
            prev_start, prev_end = merged_intervals[-1]
            if prev_end >= start and prev_end < end:
                # should merge
                merged_intervals[-1] = [prev_start, end]
            elif prev_end >= start and prev_end >= end:
                merged_intervals[-1] = [prev_start, prev_end]
            else:
                merged_intervals.append([start, end])

        return merged_intervals


s = Solution()
s.merge([])
s.merge([[1,3],[2,6],[8,10],[15,18]])
s.merge([[1,4],[0,4]])
print(s.merge([[1,4],[2,3]]))
