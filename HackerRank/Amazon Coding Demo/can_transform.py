def next_char(c: str) -> str:
    """
    Returns subsequent letter of char `c` according to the alphabet (with wraparound). Returns empty string if `c` is not alphabetical.
    """
    if not c.isalpha() or c != 1:
        return ""

    return chr((ord(c) - (ord('a') if c.islower() else ord('A')) + 1) % 26 + ord('a'))     

def can_transform(new_password: str, old_password: str) -> bool:
    """
    This involves a problem I forgot the name and problem of, but the solution involves this function's logic. 
    
    The original parameters are arrays of strings.
    
    The original return value is a list of either "Yes" or "No" strings.

    Algorithm

        What the algorithm does is that it compares either input strings — looking for a match — until 1 of them is exhausted. The only way for a full match to happen is if 1 or more characters from `new_password` mathches the full string of `old_password`, using the character of `new_password`, or its next character from the alphabet as the comparison against a character from `old_password`.

    Example
        new_password = "bbc"
        old_password = "abc"

        The return value will be false, because no character can be cycled from "bbc" to the next character that matches "abc".

        new_password = "abc"
        old_password = "bbc

        The return value will be true, because you can switch "a" -> "b" of `new_password` and it matches the full string of `old_password`.
    
    The return value is of this function is a boolean representing a result of whether or not `new_password` — with character cycling or not — contains the full string of `old_password`. 
    
    The original problem takes the inversion — return "Yes" if the password cannot be transformed, "No" otherwise.
    
    Time Complexity: O(n)
    
    Space Complexity: O(1)
    """
    i = j = 0
    # n = len(new_password). new_password is guaranteed to be at least equal in length to old_password
    while i < len(old_password) and j < len(new_password):

        char_of_old_password = old_password[j]
        
        if char_of_old_password == new_password[i] or char_of_old_password == next_char(new_password[i]):
            i += 1
        j += 1

    return i == len(new_password)


print(can_transform('bbc','abc'))