from arithmetic import is_divisible
from _04_gcf import find_factors

# Relative to Math directory.
PRIME_DIR = r"C:\Users\MICRO\Desktop\github-clones\Python\OC\Problems\Math\Arithmetic\Text\prime_numbers.txt"

def main():
    x = input("Enter number:\n")
    if (not x.isnumeric()):
        print("Input must be a number.")
        return
    x = int(x)
    assert(x > 1)

    p_factors = p_factorization(x)
    if (p_factors):

        print(p_factors)
    else:
        print(f"{x} is prime.")

    return None

def p_factorization(n: int) -> dict[int, int]:
    """Get the prime factorization of `n`.

    Args:
        n: The number to factor.

    Returns:
        A dictionary containing the prime factors (keys) of `n` in ascending order and its exponents (values).
    """
    p_factors = {}
    primes = __get_prime_nums()
    # The text file should not be empty
    assert(primes)

    primes_len = len(primes)
    ptr = 0

    while not (is_prime(n)):
        if (ptr == primes_len):
            primes.append(next_prime(primes[ptr-1]))
            primes_len+= 1

        if (is_divisible(n, primes[ptr])):
            # Perform division
            n = n//primes[ptr]

            # Record divisor
            p_factors = __record_number(p_factors, primes[ptr])
            
            # Record quotient
            if (is_prime(n)):
                p_factors = __record_number(p_factors, n)
                break

            # Reset the divisor
            ptr = 0

        else:
            ptr+= 1

    __update_prime_txt(primes)
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

def __record_number(p_factors: dict[int, int], n: int):
    if not (p_factors.get(n)):
        p_factors[n] = 1
    else:
        p_factors[n]+= 1
    return p_factors

def __get_prime_nums() -> list[int]:
    with open(PRIME_DIR, "r") as primes_txt:
        file_contents = primes_txt.read()
        primes = [int(num) for num in file_contents.strip().split(",")]
    
    return primes

def __update_prime_txt(primes: list[int]) -> None:
    primes_old = __get_prime_nums()
    primes_new = [num for num in primes if not (num in primes_old)]

    new_data = ",".join(map(str, primes_new))
    
    if (new_data):
        with open(PRIME_DIR, "a") as prime_txt:
            prime_txt.write(f",{new_data}")

    return

if __name__ == "__main__":
    main()