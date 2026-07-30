# Run this script from the parent of Arithmetic folder.
from Arithmetic._04_gcf import find_gcf

def main():
    coords1 = input("Enter coordinates for point 1:").split()
    assert(len(coords1)==2)
    p1 = int(coords1[0]), int(coords1[1])


    coords2 = input("Enter coordinates for point 2:").split()
    assert(len(coords2)==2)
    p2 = int(coords2[0]), int(coords2[1])

    m = find_slope(p1, p2)

    if m[0] == 0:
        out = "Zero (Horizontal line)"
    elif m[1] == 0:
        out = "Undefined (Vertical line)"
    else:
        out = f"{m[0]}/{m[1]}"

    print(f"Slope: {out}")
    m_perp = perp_slope(m)
    print(f"Perpendicular: {m_perp[0]}/{m_perp[1]}")

def find_slope(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    """Return the rise and the run separately of the two points in lowest form.

    Args:
        p1: First point's coordinates.
        p2: Second point's coordinates.
    """
    rise = p1[1]-p2[1]
    run = p1[0]-p2[0]

    # Remove negative from denominators.
    rise, run = correct_slope(rise, run)

    if ((gcf:= find_gcf(rise, run)) > 1):
        rise //= gcf
        run //= gcf

    return rise, run

def perp_slope(m: tuple[int, int]) -> tuple[int, int]:
    temp = m[0]
    rise = -1* m[1]
    run = temp

    return correct_slope(rise, run)

def correct_slope(rise, run):
    """Puts any negative sign onto the numerator (rise) value."""
    if run < 0:
        rise *= -1
        run = abs(run)

    return rise, run


if __name__ == "__main__":
    main()