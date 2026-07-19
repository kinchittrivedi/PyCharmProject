class Solution:
    def three_sum(self, nums: list[int], target: int) -> list[int]:

        res = []
        nums.sort()

        for i, v in enumerate(nums):
            if i > 0 and v == nums[i-1]:
                continue

            l, r = i+1, len(nums)-1
            while l<r:
                threesum = v + nums[l] + nums[r]

                if threesum > target:
                    r-=1
                elif threesum < target:
                    l+=1
                else:
                    res.append([v, nums[l], nums[r]])
                    l+=1
                    while nums[l] == nums[l-1] and l < r:
                        l+=1
        return res

sol = Solution()
print(sol.three_sum([1, 2, 3,4,5,-1,-3], 0))
