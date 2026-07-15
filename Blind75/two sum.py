#two sum problem

class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        prevnum = {} #hasmap val:index

        for i,n in enumerate(nums):
            diff = target - n
            if diff in prevnum:
                return [prevnum[diff], i]
            else:
                prevnum[n] = i

sol = Solution()
j = sol.two_sum([1, 2, 3, 4], 4)
print(j)  # Output: [0, 2]





