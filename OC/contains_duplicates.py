from radix_sort import radix_sort
from count_digits import count_digits_iterative

def contains_duplicates(array: list[int]) -> bool:
    """Finds duplicates in an array using Radix Sort."""
    pos_array = [n for n in array if n >= 0]
    max_digits_pos = count_digits_iterative(max(pos_array))
    
    neg_array = [n for n in array if n < 0]
    max_digits_neg = count_digits_iterative(min(neg_array))

    sorted_pos_array = radix_sort(pos_array, max_digits_pos)
    
    sorted_neg_array = radix_sort(neg_array, max_digits_neg)
    
    return find_duplicates(sorted_pos_array) and find_duplicates(sorted_neg_array)
    

def find_duplicates(array: list[int]) -> bool:
    """
    Returns True if duplicates in `array` found. False otherwise.
    """
    for i in range(len(array) - 1):
        if array[i] == array[i + 1]:
            return True
    return False
