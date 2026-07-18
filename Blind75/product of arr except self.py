class Solution:
    def product_of_arr(self,nums: list[int]) -> list:
        res = [1]*len(nums)

        prefix = 1
        for i in range(len(nums)):
            res[i] = prefix
            prefix*=nums[i]
        postfix = 1
        for i in range(len(nums)-1,-1,-1):
            res[i]*=postfix
            postfix*=nums[i]
        return res

product = Solution()

print(product.product_of_arr([1,2,3,4]))

