# My solution for Amazon's SDE Interview Coding Example: https://www.youtube.com/watch?v=yKz2kPip4sg
# The solution does not have any way of differentiating between 2 robots switching and 2 robots staying in the same position, it just evalautes if the time series is possible or not.

def valid_time_series(positions: list[list[int]]) -> bool:
    """
    Evaluates if a time series is valid or not.

    O(r * c)
    """
    # Handle 1 row.
    if len(positions) < 2:
        return True
    
    # Handle invalid amount of robots i.e. robots appeared or disappeared from subsequent rows or time series.
    # And handle incorrect col amount.
    if (
        any(sum(positions[0]) != sum(positions[row]) for row in range(1, len(positions))) 
        or 
        any(len(positions[0]) != len(positions[row]) for row in range(1, len(positions))) 
        ):
        return False
    
    row_amount = len(positions)
    col_amount = len(positions[0])

    # We loop through, starting at 0 (even) or 1 (odd), depending on the amount of time series.
    # The loop is incremented by 2 to maintain the odd or even state. 
    # This speeds up the looping process.
    for row in range(0 if not row_amount % 2 else 1, row_amount - 1, 2):
        # For every row, the occupied index is set to -1 or null. 
        # This variable represents the index position on the next row that cannot be taken by another robot.
        occupied_index = -1

        # We go through every position in the time series.
        for col in range(col_amount):
            # If we encounter a robot:
            if positions[row][col] == 1:
                # (1) Assume its previous location is not set.
                prev_loc = -1

                # (2) Get the previous location only if it is not the first time series.
                if row != 0:
                    prev_loc = find_next_location(col, prev_loc, positions[row - 1])

                # (3) Get the index it could have ended up in. 
                # The returned index cannot be used again.
                next_loc = find_next_location(col, occupied_index, positions[row + 1])

                # We check if the next location it ended up in is valid or not. If it is valid, it implies that we have found a position in the previous, current, or next index, that was not already occupied.
                # We also check if its previous location is valid. The only case where it could be invalid is if we are in the first row, otherwise all robots in the current row should have a previous location.
                if next_loc != -1 and (prev_loc != -1 or row == 0):
                    occupied_index = next_loc
                else:
                    return False
            
    return True

def find_next_location(curr_index, occupied_index, next_row):
    """
    The robot could only end up in 3 indices: The previous index, the current, and the next. If one of these locations is taken by a previous robot in the same row, that position is skipped.

    We start the count at the previous index since the columns in each time series is only a 1-d array, which means that the first robot's position should be the least out of all subsequent robots.

    O(3)
    """
    next_index = curr_index + 1
    # next_index + 1 should be at most equivalent to len(next_row), which means next_index should always be less than len(next_row), else we defer to the latter len(next_row). The latter value is equal across all rows.
    for i in range(curr_index - 1 if curr_index != 0 else 0, next_index + 1 if next_index < len(next_row) else len(next_row)):
        if i != occupied_index and next_row[i]:
            return i
    return -1

def main():
    print(valid_time_series(arr))
    return None

if __name__ == "__main__":
    arr = [[1,0,1], [0,1,1], [0,1,1]]
    main()