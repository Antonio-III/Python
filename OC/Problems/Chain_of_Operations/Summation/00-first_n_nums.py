"""
Make a function that returns the sum of the first n natural numbers (inclusive).
For example: f(4) should calculate 1+2+3+4 and return 10.
"""

def main() -> None:
    n = 4 # or int(input("Enter n:\n"))

    assert(n > 1)

    print(sum_first_n_nums(n))

def sum_first_n_nums(n: int) -> int:
    """
    An interface for the function. Change the function calls to execute various solutions.
    """
    # return _sum_first_n_nums_iter(n)
    # return _sum_first_n_nums_rec(n)
    return _sum_first_n_nums_pyt(n)

def _sum_first_n_nums_iter(n: int) -> int:
    """
    Iterative solution.
    """
    sum = 0
    
    for i in range(1, n+1):
        sum+=i

    return sum

def _sum_first_n_nums_rec(n: int) -> int:
    """
    Recursive solution.
    """
    if n > 1:
        return n + _sum_first_n_nums_rec(n-1)
    
    return 1

def _sum_first_n_nums_pyt(n: int) -> int:
    """
    Pythonic solution.
    """
    return sum(range(1, n+1))


if __name__ == "__main__":
    main()