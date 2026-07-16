class Solution:
    def sliding_window(self,price: list[int]) -> int:
        left,right = 0,1
        maxp = 0

        while right<len(price):
            if price[left] < price[right]:
                profit = price[right] - price[left]
                maxp = max(maxp, profit)

            else:
                left = right
            right+=1

        return maxp

profit = Solution()
print(profit.sliding_window([1,6,7,9,14]))