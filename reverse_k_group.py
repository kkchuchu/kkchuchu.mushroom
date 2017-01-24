"""
leet code: 25. Reverse Nodes in k-Group
"""

class Solution(object):
    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """
        previous = ListNode(0)
        previous.next, point = head, head
        while point:
            s = [0 for i in range(k)]
            for i in range(k):
                try:
                    s[i] = point.val
                    point = point.next
                except:
                    return head
            tmp = previous
            for i in range(k):
                tmp = tmp.next
                tmp.val = s[k-1-i]
            previous = tmp
        return head
