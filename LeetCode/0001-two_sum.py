# https://leetcode.com/problems/two-sum/description/

# The problem assumes one solution, so don't mind the type warning on return.

class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]: # pyright: ignore[reportReturnType]
        addends_and_i = {}

        for i, addend1 in enumerate(nums):
            addend2 = target - addend1

            if addend2 in addends_and_i:
                return [i, addends_and_i[addend2]]

            addends_and_i[addend1] = i


# Slower solution:
def twoSum(self, nums: list[int], target: int) -> list[int]: # pyright: ignore[reportReturnType]
        for i in range(len(nums)):
            addend1 = nums[i]
            addend2 = target - addend1

            try:
                i2 = nums.index(addend2, i+1)
            except ValueError:
                continue
            else:
                return [i, i2]