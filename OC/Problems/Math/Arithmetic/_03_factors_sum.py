from arithmetic import find_factors

def main() -> None:
    factors = input("Enter quadratic coefficient and constant:\n").split()
    assert(len(factors) == 2)

    f1, f2 = (int(n) for n in factors)

    y = int(input("Target sum:\n"))

    print(factors_sum(f1*f2, y))


def factors_sum(product: int, target_sum: int) -> tuple[int, int]:
    """Return the pair of factors of `x` that sum to `y`.
    """
    # This function is made to quickly find factors of the middle coefficient in a quadratic expression, to see if it is factorable.

    if target_sum == 0:
        return (0, target_sum)

    limit = int((abs(product)) ** 0.5)

    for f1 in range(1, limit+1):
        if (product % f1) == 0:
            f2 = product//f1
            if (f1 + f2 == target_sum):
                return (f1, f2)
            if (-f1 + f2 == target_sum):
                return (-f1, f2)
            if (f1 - f2 == target_sum):
                return (f1, -f2)
            if (-f1 - f2 == target_sum):
                return (-f1, -f2)

    return (0, 0)

if __name__ == "__main__":
    main()