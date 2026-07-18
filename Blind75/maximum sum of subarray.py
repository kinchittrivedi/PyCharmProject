class Solution:
    def Maxsubarray(self,nums: list[int]) -> int:
        maxsubarr = nums[0]
        currsum = 0

        for i in nums:
            if currsum < 0:
                currsum = 0
            currsum+=i
            maxsubarr =max(currsum,maxsubarr)
        return maxsubarr

subarr = Solution()
print(subarr.Maxsubarray([-1,2,-3,4,5,-8,-6,7]))
