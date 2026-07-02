from _04_gcf import find_factors, __is_divisible

def main():
    x = input("Enter number:\n")
    if (not x.isnumeric()):
        print("Input must be a number.")
        return
    x = int(x)
    assert(x > 0)

    p_factors = p_factorization(x)
    print(p_factors)

    return None

def p_factorization(n: int) -> dict[int, int]:
    """Get the prime factorization of `n`.

    Args:
        n: The number to factor.

    Returns:
        A dictionary containing the prime factors (keys) of `n` in ascending order and its exponents (values).
    """
    p_factors = {}
    prime = 2

    while not (is_prime(n)):
        if (__is_divisible(n, prime)):
            n = n//prime
            # Record divisor
            p_factors = record_number(p_factors,prime)
            
            # Record quotient
            if (is_prime(n)):
                p_factors = record_number(p_factors, n)

            # Reset the divisor
            prime = 2
        else:
            prime = next_prime(prime)

    return p_factors

def is_prime(n: int) -> bool:
    """Determine if `n` is a prime number or not. If `n` is prime, then the function returns `True`.
    """
    return len(find_factors(n)) == 2

def next_prime(n: int) -> int:
    """Return the next prime number after `n`. The starting number does not have to be a prime number.

    Args:
        n: The starting number.

    Returns:
        The prime number after `n`.
    """
    n+= 1

    while not (is_prime(n)):
        n+= 1

    return n

def record_number(p_factors: dict[int, int], n: int):
    if not (p_factors.get(n)):
        p_factors[n] = 1
    else:
        p_factors[n]+= 1
    return p_factors
if __name__ == "__main__":
    main()