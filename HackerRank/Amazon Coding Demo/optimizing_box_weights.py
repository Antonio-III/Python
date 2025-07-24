"""
An Amazon Coding Demo problem.
"""

#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'minimalHeaviestSetA' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY arr as parameter.
#

def minimalHeaviestSetA(arr):
    """
    Fill array A such that: 
        - A + B is equivalent to array (arr).
        - A and B have no overlapping elements.
        - sum(A) > sum(B).
        - (redundant) A must be minimal, i.e., A takes the largest elements of arr.
    """
    # Write your code here
    arr_sum = sum(arr)
    
    A = []
    A_sum = 0
    
    B = sorted(arr)
    
    while A_sum <= arr_sum - A_sum:
        heaviest = B.pop()
        
        A.append(heaviest)
        A_sum += heaviest
            
    return sorted(A)       
    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    arr_count = int(input().strip())

    arr = []

    for _ in range(arr_count):
        arr_item = int(input().strip())
        arr.append(arr_item)

    result = minimalHeaviestSetA(arr)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
