# My solution for https://www.hackerrank.com/challenges/counting-valleys/problem
#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'countingValleys' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER steps
#  2. STRING path
#

def countingValleys(steps, path):
    # Write your code here
    step_mapping = {"U": 1, "D": -1}
    altitude = 0
    valley_counted = 0
    
    for step in path:
        altitude += step_mapping[step]
        
        # A valley is encountered if the current step is Up and that 
        # this step puts us back to sea level. 
        if altitude == 0 and step == "U":
            valley_counted += 1
            
    return valley_counted
    

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    steps = int(input().strip())

    path = input()

    result = countingValleys(steps, path)

    fptr.write(str(result) + '\n')

    fptr.close()