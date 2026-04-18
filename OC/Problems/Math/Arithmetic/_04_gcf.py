"""Find the GCF between any amount of integers.

_extended_summary_
"""
def main():
    string = input("Enter numbers:\n").split()

    try:
        num_list = [int(num) for num in string]
    except ValueError as e:
        raise ValueError(f"Unwanted character in {string}") from e
    else:
        print(find_gcf(*num_list))

def find_factors(n: int, unique: bool = True) -> list[int]:
    """Find the factors of `|n|`.

    Args:
        n: An integer.
        unique: Flag for removing duplicate factors. Defaults to True.

    Returns:
        Sorted list containing the factors of `n`.
    """
    n = abs(n)
    i = 1

    factors = []
    # root d time
    while (i**2 <= n):
        q1 = n/i
        q2 = n//i
        if (q1 == q2):
            factors.append(i)
            if (q2 != i) or not unique:
                factors.append(q2)

        i += 1
    # factors space and nlogn time
    return sorted(factors)

def find_gcf(*nums: int):

    assert(nums)
    
    sorted_nums = sorted(abs(n) for n in nums)
    
    assert(__bs(sorted_nums, 0) == -1)

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

def __get_num_list_factors(nums, unique: bool = True) -> list[list[int]]:
    assert len(nums) > 0

    num_list_factors = []
    # n time
    for num in nums:
        num_list_factors.append(find_factors(num, unique))
    # n*factors space
    return num_list_factors

def __is_divisible(dividend: int, divisor: int) -> bool:
    q1 = dividend/divisor
    q2 = dividend//divisor

    return q1 == q2

def __bs(nums: list[int], x: int):
    low = 0
    high = len(nums)

    while (low < high):
        mid = (low + high)//2
        if (nums[mid] < x):
            low = mid+1
        elif (nums[mid] == x):
            return mid 
        elif (x < nums[mid]):
            high = mid
    return -1


# deprecated

def __sort_factors_by_len(num_list_factors: list[list[int]], reverse: bool = False):
    if len(num_list_factors) == 0:
        return num_list_factors
    factors_ranking = []
    for i in range(len(num_list_factors)):
        factor_len = len(num_list_factors[i])
        factors_ranking.append((factor_len, i))
    
    factors_ranking = sorted(factors_ranking, reverse=reverse)

    num_list_factors_sorted = []

    for _, i in factors_ranking:
        num_list_factors_sorted.append(num_list_factors[i])
    
    return num_list_factors_sorted


def __find_GCF_rd(num_list: list[int]) -> int:
    """Find the GCF in root(d) runtime and space.

    _extended_summary_

    Args:
        num_list: _description_

    Returns:
        _description_
    """
    assert (len(num_list) >= 2)
    assert (not "0" in num_list)

    if 0 in num_list:
        return 0

    # Numbers are sorted as POSITIVE integers
    num_list = sorted(abs(n) for n in num_list)

    num_list_factors = __get_num_list_factors(num_list)

    factors_l = len(num_list_factors)
    # Comparison starts at second factor onwards,
    factors_ptr = [1] * factors_l
    # because min GCF is guaranteed to be 1.
    gcf = 1

    limit = len(num_list_factors[0])

    while (factors_ptr[0] < limit):
        # Current factor is based on factors of smallest number in the list
        smallest_factor = num_list_factors[0][factors_ptr[0]]
        # Equality of first factor is guaranteed, so it is cached.
        eq = 1

        # Comparison to factor starts at second number onwards.
        for i in range(1, factors_l):
            if num_list_factors[i][factors_ptr[i]] < smallest_factor:
                factors_ptr[i] += 1

            elif (num_list_factors[i][factors_ptr[i]] == smallest_factor):
                eq += 1

            elif num_list_factors[i][factors_ptr[i]] > smallest_factor:
                factors_ptr[0] += 1
                break

        if (eq == factors_l):
            gcf = smallest_factor
            factors_ptr[0] += 1

    return gcf


def __find_GCF_bs(nums: list[int]) -> int:
    assert (nums)

    nums = sorted(abs(n) for n in nums)

    assert (__bs(nums, 0) == -1)
    # n*factors space.
    num_list_factors = __get_num_list_factors(nums)

    limit = len(num_list_factors[0])

    gcf = i = 1
    # k time
    while i < limit:
        factor = num_list_factors[0][i]
        # root d time
        for num_factors in num_list_factors[1::]:
            # log n time
            if __bs(num_factors, factor) == -1:
                i += 1
                break

        gcf = factor
        i += 1

    return gcf

if __name__ == "__main__":
    main()
    # print(__bs([1, 2, 3], 0))