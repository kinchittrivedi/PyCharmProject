class Solution:
    def Climbing_Stairs(self,nums:int) -> int:
        one, two = 1, 1

        for i in range(nums-1):
            temp = one
            one = one + two
            two = temp
        return one

sol = Solution()

print(sol.Climbing_Stairs(6))

