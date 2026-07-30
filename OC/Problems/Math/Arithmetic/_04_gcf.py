"""Find the GCF of any amount of integers.
"""
from .arithmetic import find_factors

def main():
    string = input("Enter numbers:\n").split()

    num_list = [eval(n) for n in string]     
    print(find_gcf(*num_list))

def find_gcf(*nums: int):
    """Return the GCF of inputted numbers.
    """
    assert(nums)
    
    sorted_nums = sorted(abs(n) for n in nums)
    
    assert(sorted_nums[0] > 0)

    poss_factors = find_factors(sorted_nums[0])
    limit = len(poss_factors)

    gcf = i = 1

    while i < limit:
        curr_factor = poss_factors[i]
        eq = 1
        for num in sorted_nums[1:]:
            if (num//curr_factor) != (num/curr_factor):
                i += 1
                break

            eq += 1

        if eq == len(nums):
            gcf = curr_factor
            i += 1

    return gcf

if __name__ == "__main__":
    main()