class Solution:
    def container_water(self,height: list[int]) -> int:
        #brute force
        res = 0

       # for l in range(len(height)):
        #    for r in range(l+1, len(height)):
         #       area = (r-l)*min(height[l], height[r])
          #      res = max(res, area)
        #return res

        l, r = 0, len(height) - 1

        while l < r:
            area = (r - l) * min(height[l], height[r])
            res = max(res, area)

            if height[l] < height[r]:
                l+=1
            else:
                r-=1
        return res

sol = Solution()

print(sol.container_water([1, 2, 3,4,5,6,7]))