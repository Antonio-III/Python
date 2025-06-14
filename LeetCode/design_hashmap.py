# My solution for https://leetcode.com/explore/learn/card/hash-table/182/practical-applications/1140/

class MyHashMap:
    
    class Bucket(list):
            # 2d array was a temp variable to represent the bucket's data structure for this problem's context. Will keep it anyway.
            def __init__(self, array=[]):
                super().__init__()

                self.extend(list(array))

            def keys(self) -> list[int]:
                """
                Obtains keys of the given bucket. That is, the 1st element of every pair in the bucket.

                Steps: α. Where α = n elements (<= 10^4) / b (fixed 10007) ≈ 0.9993.

                Average: O(α)

                Worst: O(n)
                """
                return [pair[0] for pair in self] if len(self) else []
            
    def __init__(self):
        self.bucket_count = 10007
        self.hash_map = [self.Bucket() for _ in range(self.bucket_count)]
    def put(self, key: int, value: int) -> None:
        """
        Insert a pair or replace.
        
        Steps: 1 + α + α + (α or 1) + 1 + (1 or (1 amortised + 1))

        Average: O(α)

        Worst: O(n)
        """
        bucket = self.hash_map[key % self.bucket_count] # +1
        bucket_keys = bucket.keys() # +α

        index_of_pair = bucket_keys.index(key) if key in bucket_keys else -1 # α + (α or 1)
        
        # 1 + ( 1 or (1 amortised + 1) )
        bucket[index_of_pair][1] = value if index_of_pair != -1 else bucket.append([key, value]) or value


    def get(self, key: int) -> int:
        """
        Get value-pair of a key.
        
        Steps: 1 + 1 + α + α + (α or 1) + 1

        Average: O(α)

        Worst: O(n)
        """
        index = key % self.bucket_count # +1

        bucket = self.hash_map[index] # +1
        bucket_keys = [bucket[i][0] for i in range(len(bucket))] # +α
        
        index_of_pair = bucket_keys.index(key) if key in bucket_keys else -1 # α + α or 1
        
        result = bucket[index_of_pair][1] if index_of_pair != -1 else -1 # +1
        
        print(result)
        
        return result
    
    def remove(self, key: int) -> None:
        """
        Remove pair using key.
        
        Steps: 1 + 1 + α + (α or 1) + α + (α or 1)

        Average: O(α)
        
        Worst: O(n)
        """
        index = key % self.bucket_count # +1
        
        bucket = self.hash_map[index] # +1
        bucket_keys = [bucket[i][0] for i in range(len(bucket))] # +α
        
        index_of_pair = index_of_pair = bucket_keys.index(key) if key in bucket_keys else -1 # α + α or 1
        
        bucket.pop(index_of_pair) if key in bucket_keys else None # α + α or 1