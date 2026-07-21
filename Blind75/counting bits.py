class Solution:
    def Countingbits(self,num: int) -> list[int]:
        dp = [0]*(num+1)
        offset = 1

        for i in range(1,num+1):
            if offset*2 == i:
                offset = i
            dp[i] = 1 + dp[i - offset]

        return dp

sol = Solution()

print(sol.Countingbits(7))


