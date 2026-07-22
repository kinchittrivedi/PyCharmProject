class Solution:
    def Reversebits(self,num: int) -> int:
        res = 0

        for i in range(4):
            bit = (num>>i) & 1
            res = res | (bit << (3-i))
        return res

sol = Solution()

print(sol.Reversebits(4))

