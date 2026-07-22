class Solution:
    def Missingnumber(self,num: list[int]) -> int:
        res = len(num)

        for i in range(len(num)):
            res+=(i - num[i])
        return res

sol = Solution()

print(sol.Missingnumber([0,1,2,3,5,6,7,8]))
