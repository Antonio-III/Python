from math import sqrt

THOUSANDTH = 3
H_THOUSANDTH = 5
NDIGITS = THOUSANDTH

def main() -> None:
    x = float(input("Enter number:\n"))
    out = round(sqrt(x), NDIGITS)
    print(f"√{x} = {out}")
if __name__ == "__main__":
    main()