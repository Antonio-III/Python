# A script that solves this problem (https://www.hackerrank.com/challenges/fun-game-1/problem).
def funGame(a: list[int], b: list[int]) -> str:
    """
    Returns results of a game using an algorithm that finds the index whose value is the highest between 2 arrays.
    """
    # Score 
    P1, P2 = 0, 0
   
    # P1 starts, per game rules
    starting_turn = 'P1'

    # Game length is equal to the length of the array. Each iteration can only have 1 player acting.
    for _ in range(len(a)):
        
        # Find best index. The best index is the highest value in either arrays.
        i = find_most_optimal_move(a, b)

        if starting_turn == 'P1':
            P1 += a[i]
            # Next iteration goes to the other player
            starting_turn = 'P2'
        else:
            P2 += b[i]
            starting_turn = 'P1'

        # Remove the picked elements before the next player's turn.
        a.pop(i)
        b.pop(i)

    return 'First' if P1 > P2 else ('Second' if P2 > P1 else 'Tie')

def validate_range_inclusive(val: int, min_range: int, max_range: int) -> int:
    """
    Checks if val passes the constraints of the problem. Returns val if pass. Raises an error if fail. 
    """
    if not (min_range <= val <= max_range):
        raise ValueError(f'{val} out of range [{min_range}, {max_range}].')
    return val

def get_T_value() -> int:
    """
    Returns error-free T that matches the constraints.
    """
    constraints = 1, 10
    try:
        # Enforces T must be int.
        t = int(input().strip())
    except ValueError as e:
        raise e
    else:
        # Constraint for `1 <= T <= 10` is enforced.
        return validate_range_inclusive(t, *constraints)

def get_n_value() -> int:
    """
    Returns error-free n that matches the constraints.
    """
    constraints = 1, 1000
    try:
        n = int(input().strip())
    except ValueError as e:
        raise e
    else:
        return validate_range_inclusive(n, *constraints)
    
def get_ab_value() -> tuple[list[int], list[int]]:
    """
    Return error-free arrays a and b that matches the constraints.
    """
    constraints = 1, 10**5
    try:
        a = [validate_range_inclusive(int(char), *constraints) for char in input().rstrip().split()]
        b = [validate_range_inclusive(int(char), *constraints) for char in input().rstrip().split()]
    except ValueError as e:
        raise e
    else:
        if len(a) != len(b):
            raise ValueError(f"Array a and b must be equal in length: len(a)={len(a)}. len(b)={len(b)}.")
        return a, b 

def find_most_optimal_move(a: list[int], b: list[int]) -> int:
    """
    Return an index whose value, when both arrays are combined, is the highest.
    """
    best_gain = 0
    best_index = -1
    for i in range(len(a)):
        gain = sum([a[i] + b[i]]) 

        if gain > best_gain:
            best_gain = gain
            best_index = i

    return best_index


if __name__ == '__main__':

    t = get_T_value()

    for t_itr in range(t):
        
        n = get_n_value()
            
        a, b = get_ab_value()
      
        result = funGame(a, b)
        
        print(result)