def next_char(c: str) -> str:
    return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))     

def can_transform(new_password: str, old_password: str) -> bool:
    """
    This involves a problem I forgot the name and problem of, but the solution involves this logic. 
    
    The original parameters are arrays of strings.
    
    The original return value is a list of either "Yes" or "No".

    Solution

        What the algorithm does is that it compares either input strings until 1 of them is exhausted. The only way for a full match to happen is if 1 or more characters from `new_password` mathches the full string of `old_password`, using the character of `new_password`, or its next character from the alphabet as the comparison against a character from `old_password`.

    Consider
        new_password = "bbc"
        old_password = "abc"

        The return value will be false, because no character can be cycled from "bbc" to the next character that matches "abc".

        new_password = "abc"
        old_password = "bbc

        The return value will be true, because you can switch "a" -> "b" of `new_password` and it matches the full string of `old_password`.
    """
    i = j = 0
    while i < len(old_password) and j < len(new_password):
        chars_of_new_password = [new_password[i], next_char(new_password[i])]
        char_of_old_password = old_password[j]
        
        if char_of_old_password in chars_of_new_password:
            i += 1
        j += 1
    return i != len(new_password)


print(can_transform('bbc','abc'))