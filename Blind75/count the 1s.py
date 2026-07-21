class Solution:
    def Hammingweight(self,num: int) -> int:
        res = 0

        #while num:
        #    res+=num%2
        #    num = num >> 1
        #return res

        while num:
            num&=(num-1)
            res+=1
        return res
