class Solution:
    def contains_duplicate(self,nums: list[int]) -> bool:
        hashset = set()

        for n in nums:
            if n in hashset:
                return True
            hashset.add(n)
        return False

hashset = Solution()
print(hashset.contains_duplicate([1,2,4,5,7,3]))


