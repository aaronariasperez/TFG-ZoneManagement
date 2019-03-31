

class Solution(object):
    def recursivee(self, nums1, nums2, steps, esPar, last1, last2, i, j):
        if esPar and steps == ((len(nums1) + len(nums2)) / 2)+1:
            return (last1 + last2) / 2
        elif not esPar and steps == ((len(nums1) + len(nums2)) // 2) + 1:
            return last1
        else:
            if i != len(nums1):
                if nums1[i] <= nums2[j]:
                    last2 = last1
                    last1 = nums1[i]
                    return self.recursivee(nums1, nums2, steps + 1, esPar, last1, last2, i + 1, j)
            elif j != len(nums2):
                last2 = last1
                last1 = nums2[j]
                return self.recursivee(nums1, nums2, steps + 1, esPar, last1, last2, i, j + 1)


    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        esPar = True if (len(nums1) + len(nums2)) % 2 == 0 else False
        return self.recursivee(nums1, nums2, 0, esPar, 0, 0, 0, 0)

sol = Solution()
a = sol.findMedianSortedArrays([1,2],[3,4])
print(a)