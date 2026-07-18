class Solution:
    def MaxProduct(self,nums: list[int]) -> int:
        res = max(nums)
        curMax, curMin = 1,1

        for n in nums:
            if n == 0:
                curMax, curMin = 1, 1
                continue

            temp = n*curMax
            curMax = max(n*curMax,n*curMin,n)
            curMin = min(temp,n*curMin,n)

            res = max(res, curMax)
        return res

product = Solution()

print(product.MaxProduct([-1,1,2,-3,-4,-5,6]))





