# My solution for https://leetcode.com/explore/learn/card/hash-table/182/practical-applications/1140/

class MyHashSet:
    class Bucket(list):
        def __init__(self, convertible_to_list=[]):
            super().__init__()

            self.extend(list(convertible_to_list))
            
    def __init__(self):
        # Bucket size will fit the constraint (10^4) and be a prime number.  
        self.bucket = 10007
        
        self.hash_set = [self.Bucket() for _ in range(self.bucket)]

    def add(self, key: int) -> None:
        """
        Add key to hash set. 
        
        Steps: 1 + α + 1 (amortized), where α = n (at most 10^4) / b (fixed 10007). Initial +1 is the index calculation.
        Average: O(1) because 10^4/10007 ≈ 0.9993.
        Worst: O(n).
        """
        # index corresponds to which bucket a key will be mapped onto.
        index = key % self.bucket
        
        self.hash_set[index].append(key) if key not in self.hash_set[index] else None
        
    def remove(self, key: int) -> None:
        """
        Remove key from hash set.
        
        Steps: 1 + 3α, due to membership test (α), and removal (2α, scan & shift (remove)).
        Average: O(1).
        Worst: O(n).
        """
        index = key % self.bucket
        
        self.hash_set[index].remove(key) if key in self.hash_set[index] else None
        
    def contains(self, key: int) -> bool:
        """
        Membership test if key is in set object.
        
        Steps: 1 + α.
        Average: O(1).
        Worst: O(n).
        """
        index = key % self.bucket
        
        return key in self.hash_set[index]