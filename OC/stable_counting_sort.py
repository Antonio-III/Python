# Python script that performs a counting sort algorithm.

def stable_counting_sort(array: list[int], base: int = 10, power_of_base: int = 0):
    """
    Performs the Stable Counting Sort algorithm, which sorts the array by the given `place_value`.

    Example uses:
        1. stable_counting_sort([2, 1, 5, 4, 2], 1) -> [1, 2, 2, 4, 5]
        2. stable_counting_sort([76, 98, 14, 13, 56], 10) -> [1, 2, 2, 4, 5]\
    """
    place_value = base**(power_of_base)

    # The output array. Starts as the length of the input array but whose values are null or 0.
    out = [0] * len(array)

    # Base 10 has 10 symbols. We want to be able to count how many of each symbols we have encountered.
    count = [0] * base

    # In base 10, count the occurrences numbers 0, 1, 2, 3, 4, 5, etc.. in the place_value and store it in their respective index indices. (Indices are equivalent to the numbers themselves). 
    for num in array:
        # Check what number is in the place_value of a given element. For instance, this step could check what number is in the tens place of 456. It is 5, and so an incremenent will be put into count[5]
        symbol = (num // place_value) % base
        count[symbol] += 1

    """
    Once we have counted the amount of times we have seen every symbol in the base, we now reinterpret `count` to represent the index position of each symbol's sighting. In the docstring, you will see that count[0] means that 0 is in the 1st place of the output array. count[1] will be in the 2nd place. count[2] at 3rd. count[3] and count[4] are at 3rd as well but since because we never encountered them anyway, we won't have to use their values. Finally, count[5] at 4th place. 

    All this to say: "In counting sorting at ones place using array [12, 345, 4890, 1], the number with a 0 will be 1st, the number with a 1 will be 2nd, 2 will be 3rd and 5 will be 4th".

    array = [12, 345, 4890, 1]
    count = [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0] ->  [1, 2, 3, 3, 3, 4, 4, 4, 4, 4]
    """
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    """
    array = [12, 345, 4890, 1]
    count = [1, 2, 3, 3, 3, 4, 0, 0, 0, 0]
    out = [4890, 1, 12, 345]

    Evaluate the index positions of every number according to the sort.
    
    When we counted unique symbols, we incremented the counter corresponding to that symbol. We then modified this value to represent the resulting index positions of our numbers. In the case of numbers with the same symbols like [21, 11, 31], the outcome should stay as is, as there is no reason for them to be ordered othewise. To account for this, we have to traverse the original array in reverse order. That is to say we evaluate the array as "first in, last out". 
    # This has to do with our counting method, in that we counted +1 when we saw "1" in 21, and another +1 when we saw "1" in 11, and so on. If we traverse the array as "first in, first out", when we evaluate 21's position in the resulting array, due to our counting, 21's position will be interpreted as the 3rd encounter of the number "1", rather than the 1st.
    """
    for num in array[::-1]:
        symbol = (num // place_value) % base

        out[count[symbol] - 1] = num
        count[symbol] -= 1

    return out