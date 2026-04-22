from math import sqrt

# Index values, and integers.
THOUSANDTH = 3
H_THOUSANDTH = 5

NDIGITS = THOUSANDTH


STR_ROUNDING = [
    "Tenths",
    "Hundredths",
    "Thousandths",
    "Ten Thousandths"
    "Hundred Thousandths"
]


def main() -> None:
    x = float(input("Enter number:\n"))
    out = sqrt(x)
    print(f"√{x} = {out}")
    print(f"Nearest {STR_ROUNDING[NDIGITS-1]} ≈ {round(out, NDIGITS)}")
if __name__ == "__main__":
    main()