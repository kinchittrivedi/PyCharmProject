class Solution:
    def SearchRotatedSortedArr(self,nums: list[int], target:int) -> int:
        l, r = 0, len(nums)-1

        while l <= r:
            mid = (l + r)//2
            if nums[mid] == target:
                return  mid

            #left sorted arr

            if nums[l]<=nums[mid]:
                if target > nums[mid] or nums[l]>target:
                    l = mid + 1
                else:
                    r = mid - 1

            #right sorted arr

            else:
                if target < nums[mid] or nums[r]< target:
                    r = mid - 1
                else:
                    l = mid + 1
        return -1

rotate = Solution()

print(rotate.SearchRotatedSortedArr([0,1,2,3,-2,-1], -1))
