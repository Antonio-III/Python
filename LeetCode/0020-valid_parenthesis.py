# https://leetcode.com/problems/valid-parentheses/

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        # The pairs are mapped as close:open due to how parenthesis-matching will be resolved. 
        pairs = {
            ")": "(", 
            "}": "{", 
            "]": "["}
        
        for c in s:
            # Record opening pairs.
            if c not in pairs:
                stack.append(c)
                continue
            
            # Closing pairs encountered:

            # The last opening parenthesis on the list
            active_p = stack.pop() if stack else "_"

            # If the type of the closing parenthesis does not match the type of the last recorded opening parenthesis, then the string is fundamentally not a valid parenthesis sequence, so we can exit early. The stack has also been altered, so the stack is of no use to future pair-matching anyway.
            if pairs[c] != active_p:
                return False
            
        # Though the string is exhausted, we still need to check the length of our list so as to avoid giving false-positives to strings who only consist of opening parentheses.
        return len(stack) == 0


# Alternative solution:

# This solution is quadratic O(n^2) time because `.replace` performs a linear scan inside a roughly linear time (`while`) loop.
def isValid_2(s: str) -> bool:
        old_len = -1
        new_len = 0

        while old_len != new_len and len(s) >= 1:

            old_len = new_len

            s = s.replace("()","").replace("{}","").replace("[]","")

            new_len = len(s)

            
        return len(s) == 0