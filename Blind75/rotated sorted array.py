class Solution:
    def MinRotatedSortedArr(self,nums: list[int]) -> int:
        left, right = 0, len(nums)-1
        res = 0

        while left <= right:
            if nums[left]<nums[right]:
                res = min(res,nums[left])
                break

            mid = (left + right) // 2
            res = min(res,nums[mid])
            if nums[mid]>=nums[left]:
                left = mid+1
            else:
                right = mid-1

        return res

rotate = Solution()

print(rotate.MinRotatedSortedArr([0,1,2,3,-2,-1]))
