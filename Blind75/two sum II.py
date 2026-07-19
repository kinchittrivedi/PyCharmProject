class Solution:
    def two_sum_II(self, nums: list[int], target: int) -> list[int]:

        l, r = 0, len(nums) - 1

        while l < r:
            currSum = nums[l] + nums[r]

            if currSum > target:
                r-=1
            elif currSum < target:
                l+=1
            else:
                return [l,r]

sol = Solution()
print(sol.two_sum_II([1, 2, 3, 4], 4))

