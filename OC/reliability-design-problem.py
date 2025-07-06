"""
A script that solves a reliability design problem. 
Based on: https://www.youtube.com/watch?v=uJOmqBwENB8&pp=ygUacmVsaWFiaWxpdHkgZGVzaWduIHByb2JsZW0%3D

Table of Contents:
    main
    solv_reliability_design
        get_rc_for_all_devices
        copy_for_all_devices
    find_upper_bound
        inputs_are_valid (checker)
    create_table
    replace_row
    insert_row
    replace_col
    extract_col
    d_first_key_is_k
    apply_dominance_rule
        get_all_pairs_in_asc_r
        get_bad_pairs
        remove_bpairs_from_d
    del_dict_key_w_empty_val
    rc_pairs_in_nth_main_set
        inputs_are_valid
    get_subsets_only_from_all_sets
    main_set_of_rc_pair
    subset_of_rc_pair
    subset_of_rc_pair_
    find_rc_pair_index_in_all_subsets
    subsets_under_nth_main_set
    len_args_not_equal_to_num
    convert_input_to_list_of_ints
    convert_input_to_list_of_floats
    convert_input_to_int
    len_args_equal_to_len_comp
"""
from typing import Any

def main() -> None:
    c = 0
    devices = 0
    cost = []
    reliability = []
    try:
        c = convert_input_to_int(text="Enter amount of capital:\n")
        devices = convert_input_to_int(text="Enter number of devices:\n")
        
        cost = convert_input_to_list_of_ints(text="Enter cost per row. Example input: 30, 40, 50\n", sep=",")
        reliability = convert_input_to_list_of_floats(text="Enter reliability per row. Example input: 0.9, 0.8, 0.7\n", sep=",")

        if len_args_not_equal_to_num(cost, reliability, num=devices):
            raise RuntimeError("cost or reliability must be the same length as the amount of devices.")
        
    except KeyboardInterrupt:
        pass 

    output = solv_reliability_design(c=c, devices=devices, cost=cost, reliability=reliability, starting_set=STARTING_SET)
    print(output)

def solv_reliability_design(c: int, devices: int, cost: list, reliability: list, starting_set: dict) -> tuple[dict, tuple]:
    def get_rc_for_all_devices(devices: int, c_i: list, r_i: list, u_i: list, starting_set: dict):
        all_sets = starting_set
        for d in range(devices):
            curr_subset = {}

            curr_set_num = f"S^{d+1}"
            prev_set_num = f"S^{d}"

            
            for j in range(u_i[d]):
                copy_in_curr_d = j + 1

                subset_name = f"{curr_set_num}_{copy_in_curr_d}"
                curr_subset[subset_name] = []
                
                r_of_curr_item = 1 - (1-r_i[d])**copy_in_curr_d
                c_of_curr_item = c_i[d] * copy_in_curr_d

                
                len_of_prev_main_set = len(all_sets[prev_set_num])

                for l in range(len_of_prev_main_set):
                    copy_in_prev_set = l + 1

                    prev_subset_obj = all_sets[prev_set_num][f"{prev_set_num}_{copy_in_prev_set if not d_first_key_is_k(d=all_sets, k=prev_set_num) else 0}"]

                    len_of_prev_subset = len(prev_subset_obj)

                    for k in range(len_of_prev_subset):
                    
                        kth_tuple_in_prev_subset = prev_subset_obj[k]
                        
                        r_of_kth_tuple_in_prev_subset = kth_tuple_in_prev_subset[0]
                        c_of_kth_tuple_in_prev_subset = kth_tuple_in_prev_subset[1]


                        R, C =  round(r_of_kth_tuple_in_prev_subset*r_of_curr_item, ROUND_N_PLACES), c_of_kth_tuple_in_prev_subset + c_of_curr_item 

                        c_of_curr_and_next_item = C if d + 1 == devices else C + c_i[d+1]

                        if c_of_curr_and_next_item <= c:
                            curr_subset[subset_name].append((R,C))

            merged_n_purged_subset = apply_dominance_rule(d=curr_subset)
            d_cleaned = del_dict_key_w_empty_val(d=merged_n_purged_subset)

            all_sets[curr_set_num] = d_cleaned
            
        return all_sets
    
    def copy_for_all_devices(devices:int,highest_r_rc_pair:tuple[float,int],all_main_sets:dict[str,list[tuple[float,int]]],all_subsets:dict[str,list[tuple[float,int]]]):
        d = {}
        prev_rc_pair = highest_r_in_last_device
        copy = subset_of_rc_pair(rc_pair=highest_r_rc_pair, all_subsets=all_subsets)
        d[f"D{devices}"] = copy

        
        for i in range(devices-1, 0, -1):
            index_of_prev_rc_pair = find_rc_pair_index_in_all_subsets(rc_pair=prev_rc_pair, all_subsets=all_subsets)
            next_rc_pair = all_main_sets[f"S^{i}"][index_of_prev_rc_pair]
            copy = subset_of_rc_pair(rc_pair=next_rc_pair,all_subsets=all_subsets)
            d[f"D{i}"] = copy
            prev_rc_pair = next_rc_pair
        return d
    
    D_i = [f"D_{i}" for i in range(1, devices+1)]
    U_i = find_upper_bound(c=c, cost=cost)

    table = create_table(rows=devices+1, columns=COLUMNS)

    table = replace_row(table=table, pos=1, value=HEADER_COLS)

    table = replace_col(table=table, pos=1, new_value=D_i, ignore_header=True)
    table = replace_col(table=table, pos=2, new_value=cost, ignore_header=True)
    table = replace_col(table=table, pos=3, new_value=reliability, ignore_header=True)
    table = replace_col(table=table, pos=4, new_value=U_i, ignore_header=True)

    c_i = extract_col(table=table, pos=2, ignore_header=True)
    r_i = extract_col(table=table, pos=3, ignore_header=True)
    u_i = extract_col(table=table, pos=4, ignore_header=True)
    
    all_sets = get_rc_for_all_devices(devices=devices, c_i=c_i, r_i=r_i, u_i=u_i, starting_set=starting_set)
    all_main_sets = get_main_set_from_all_sets(all_sets=all_sets)
    all_subsets = get_subsets_only_from_all_sets(all_sets=all_sets)

    highest_r_in_last_device = max(rc_pairs_in_nth_main_set(n=devices,all_sets=all_sets))
    copies=copy_for_all_devices(devices=devices,highest_r_rc_pair=highest_r_in_last_device,all_main_sets=all_main_sets,all_subsets=all_subsets)

    return copies,highest_r_in_last_device


def find_upper_bound(c: int, cost: list) -> list[int]:
    """ 
    1. The functions fills in the values for the column `U_i` in the table:
        D_i | C_i | r_i | U_i
        ____|_____|_____|____
    """
    def inputs_are_valid(**kwargs):
        """ 
        1. Main function will not run unless `c` is at least equal to the sum of `cost`.
        """
        if kwargs["c"] >= sum(kwargs["cost"]):
            return True
        else:
            raise ValueError("`c` should not be lower than the summation of `cost`.")

    if inputs_are_valid(c=c, cost=cost):
        sum_of_cost = sum(cost)
        return [ ((c-sum_of_cost) // c_i) + 1  for c_i in cost]
    return []

def create_table(rows: int, columns: int) -> list[list[int]]:
    """
    1. Create a list containing `row` amount of child lists with `columns` amount of `0`  
    2. Example: create_table(2,3) returns:
        [[0,0,0],[0,0,0]]
            ^        ^
            |        |
            row 1    row 2

    3. The table can also be interpreted as:
        row 1 -> [[0,0,0],
        row 2 -> [0,0,0]]
    """
    return [ [0 * j for j in range(columns)] for _ in range(rows)]

def replace_row(table: list, pos: int, value: list) -> list[list[Any]]:
    """
    1. Replaces `pos`th row from `table`. 
        1. `pos` is 1-indexed as an argument and is adjusted to be 0-indexed. Any reference to `pos` from this point on is 0-index.
    2. Replacing a row overwrites previous data in `table[pos]`.
    3. Example: replace_row(table=table,pos=1,value=[1,2,3]) returns:
        [[1,2,3],
        [0,0,0]]
    """
    pos -= 1
    if len_args_equal_to_len_comp(value, comp=table[pos]):
        try:
            table[pos] = value
        except IndexError:
            print(f"Row index {pos} in table does not exist.")
            return []
        else:
            return table
    return []

def insert_row(table: list, pos: int, value: list) -> list[list[Any]]:
    """
    1. Insert a list in table's `pos-1`th index. 
        1. `pos` is 1-indexed as an argument and is adjusted to be 0-indexed. Any reference to `pos` from this point on is 0-index.
    2. Performs `table.insert(pos-1,value)`, and returns table.
    """
    pos-=1
    table.insert(pos,value)
    return table

def replace_col(table: list, pos: int, new_value: list,ignore_header: bool) -> list[Any]:
    """
    1. Replaces `pos-1`th column in table with `value` (list). 
        1. `pos` is 1-indexed as an argument and is adjusted to be 0-indexed. Any reference to `pos` from this point on is 0-index.
    2. Has an option to ignore header.
        Ignoring header means to slice table as table[1:] instead of table[:].
    """
    pos-=1
    for row,new_val in zip(table[1:] if ignore_header else table[:],new_value):
        row[pos]=new_val
    return table

def extract_col(table:list,pos:int,ignore_header:bool)->list[Any]:
    """
    1. Return a list of elements in the `n-1`th position of every row.
        1. `pos` is 1-indexed as an argument and is adjusted to be 0-indexed. Any reference to `pos` from this point on is 0-index.
    2. Has an option to ignore the first row (ignore_header:bool).
    3. Example: extract_col(table=table,n=1,ignore_header=True):
        1. if table =  [[1,2,3],
                       [4,5,6],
                       [7,8,9]]
        2. return: [4,7].
    """
    pos-=1
    return [ row[pos] for row in (table[1:] if ignore_header else table[:]) ]

def d_first_key_is_k(d: dict, k: Any) -> bool:
    """
    1. Returns True if `k` is the first key in dict `d`, else False.
    """
    return list(d.keys())[0]==k

def apply_dominance_rule(d: dict) -> dict[str, list[tuple[float, int]]]:
    """
    1. Return `d` with removed (R,C) values that end up having lower R & higher C when merged.
    2. In Reliability Design, (R,C) values in the merged set (not Python `set()` objects) that have a lower R & higher C than the next pair are removed.
    3. This function sorts all (R,C) values in `d` (usually a dict of subsets) in ascending order, and pairs who meet the condition for removal are removed from `d`.
        1. Example inputs: 
            1. {'S^2_1': [(0.72, 45)], 'S^2_2': [(0.864, 60)], 'S^2_3': [(0.8928, 75)]}
            2. {'S^3_1': [(0.36, 65), (0.432, 80)], 'S^3_2': [(0.54, 85), (0.648, 100)]}
    4. Example:
        1. d = {'S^3_1': [(0.36, 65), (0.4464, 95)], 'S^3_2': [(0.54, 85), (0.648, 100)]}
        2. all_pairs = [(0.36, 65), (0.4464, 95), (0.54, 85), (0.648, 100)]
        3. bad_pairs = [(0.4464, 95)]
        4. return: {'S^3_1': [(0.36, 65)], 'S^3_2': [(0.54, 85), (0.648, 100)]}.
                1. (0.4464, 95) is gone from S^3_1.
    5. Example 2:
        1. d = {'S^3_2': [(0.54, 85), (0.648, 100)], 'S^3_3': [(0.63, 105)]}
        2. all_pairs = [(0.54, 85), (0.63, 105), (0.648, 100)]
        3. bad_pairs = [(0.63, 105)]
        4. return: {'S^3_2': [(0.54, 85), (0.648, 100)], 'S^3_3': []}
            1. (0.63, 105) is gone, and the key S^3_3 is left a list with no elements.
    """
    def get_all_pairs_in_asc_r(d: dict[str, list[tuple[float, int]]]) -> list[tuple[float, int]]:
        """
        1. Returns an ascending list of (R,C) value in `d`.
        2. Example: 
            1. If d = {'S^2_1': [(0.72, 45)], 'S^2_2': [(0.864, 60)], 'S^2_3': [(0.8928, 75)]}
            2. return: [(0.72, 45), (0.864, 60), (0.8928, 75)].
        """
        return sorted([rc_pair for subset in d.keys() for rc_pair in d[subset] ])
    
    def get_bad_pairs(asc_r_pairs: list[tuple[float, int]]) -> list[tuple[float, int]]:
        """
        1. Get a list of pairs in the ascending pairs list who have lower R & higher C than the next pair.
        2. Example:
            1. if asc_r_pairs = [(0.432, 80), (0.4464, 95), (0.54, 85)]
            2. return: [(0.4464, 95)].
                This is because this pair has lower R & higher C than the next pair (0.54, 85).
        """
        bad_pairs = []

        for i in range(len(asc_r_pairs)):
            curr_pair = asc_r_pairs[i]
            prev_pair = (0,0) if i==0 else asc_r_pairs[i-1]

            curr_r, curr_c = curr_pair
            prev_r, prev_c = prev_pair

            if (prev_r <= curr_r) and (prev_c >= curr_c):
                bad_pairs.append(prev_pair)

        return bad_pairs   

    def remove_bpairs_from_d(d: dict[str, list[tuple[float, int]]], bad_pairs: list[tuple[float, int]]) -> dict[str, list[tuple[float, int]]]:
        """
        1. If a pair in `d` appears in the `bad_pairs` list, it is removed from `d`.
        2. The bad (R,C) value is also removed from the d[subset] & bad_pairs list. 
        3. Example:
            1. d = {'S^3_1': [(0.36, 65), (0.432, 80), (0.4464, 95)], 'S^3_2': [(0.54, 85), (0.648, 100)]}
            2. bad_pairs = [(0.4464, 95)]
            3. return: {'S^3_1': [(0.36, 65), (0.432, 80)], 'S^3_2': [(0.54, 85), (0.648, 100)]}.
                1. (0.4464, 95) is gone from S^3_1.
        """
        for subset in d.values():
            for rc_pair in subset[:]:
                if rc_pair in bad_pairs[:]:
                    subset.remove(rc_pair)
                    bad_pairs.remove(rc_pair)

        return d
    
    all_pairs = get_all_pairs_in_asc_r(d=d)
    bad_pairs = get_bad_pairs(asc_r_pairs=all_pairs)

    return remove_bpairs_from_d(d=d, bad_pairs=bad_pairs)

def del_dict_key_w_empty_val(d: dict) -> dict[Any, Any]:
        """
        1. Returns `d` with removed {k:v} pairs if v is empty.
            1. "Empty" means len(v)==0.
        2. Example:
            1. d = {1: [1], 2: []}
            2. return: {1: [1]}
                1. Since d[2] refers to an empty list, this pair is now removed.
        """
        d_copy = d.copy()
        for key in d_copy.keys():
            if len(d_copy[key]) == 0:
                del d[key]
        return d

def rc_pairs_in_nth_main_set(n: int, all_sets: dict[str, dict[str, list[tuple[float, int]]]]) -> list[tuple[float,int]]:
    # May need a rework
    """
    1. Gets all the (R,C) values of a subset under the `n`th main set, and return all the collected pairs in a list.
    2. Example:
        1. n = 2
        2. all_sets = {'S^0': {'S^0_0': [(1, 0)]}, 'S^1': {'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}, 'S^2': {'S^2_1': [(0.72, 45), (0.792, 75)], 'S^2_2': [(0.864, 60)]}}
        3. return: [(0.72, 45), (0.792, 75), (0.864, 60)].
            1. These values were under the subsets that belong to the second main set (`S^2`).
    """
    def inputs_are_valid(n: int, all_sets: dict) -> bool:
        """
        1. Check if `n` is at most, equal to `len(all_sets)-1`.
            1. Returns True if True, else raise ValueError.
        """
        if n <= len(all_sets) - 1:
            return True
        else:
            raise ValueError("`n` value cannot be equal to length of `all_sets`.")
        
    if inputs_are_valid(n=n, all_sets=all_sets):
        l = []
        main_set_name = f"S^{n}"
        for subset in all_sets[main_set_name]:
            l += all_sets[main_set_name][subset]
            
        return l
    return []

def get_subsets_only_from_all_sets(all_sets: dict[str, dict[str,list[tuple[float, int]]]]) -> dict[str, list[tuple[float, int]]]:
    """
    1. Return a dict containing only subsets as keys and their respective (R,C) pair as values.
    2. Example:
        1. all_sets = {'S^0': {'S^0_0': [(1, 0)]}, 'S^1': {'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}}
        2. return: {S^0_0: [(1, 0)], 'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}
            1. The main sets S^0 and S^1 have been removed, with only subsets remaining.
    """
    return {k:v for value in all_sets.values() for k,v in value.items()}

def get_main_set_from_all_sets(all_sets: dict[str, dict[str, list[tuple[float, int]]]]) -> dict[str, list[tuple[float, int]]]:
    """
    1. Return a dict containing main sets as keys and their subsets' (R,C) pair as values.
    2. Example:
        1. all_sets = {'S^0': {'S^0_0': [(1, 0)]}, 'S^1': {'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}}
        2. return: {'S^0': [(1, 0)], 'S^1': [(0.9, 30), (0.99, 60)]}
            1. The subset names are removed and the main sets contain their subsets' values directly.
    """
    return {main_set: [rc_pairs for subset in subsets.values() for rc_pairs in subset] for main_set, subsets in all_sets.items()}

def main_set_of_rc_pair(rc_pair: tuple[float, int], all_main_sets: dict[str, list[tuple[float, int]]]) -> int:
    """
    1. Return an 'int' that corresponds to the set number (0-indexed) an (R,C) pair belongs to. If there are duplicate values, the main set of the first match is returned.
    2. Example: 
        1. rc_pair = (0.8928, 75)
        2. all_main_sets = {'S^0': [(1, 0)], 'S^1': [(0.9, 30), (0.99, 60)], 'S^2': [(0.72, 45), (0.864, 60), (0.8928, 75)]}
        3. Return: 2
            1. The first match the pair (0.8928, 75) had was with main set S^2, which is main set 2 (the 3rd out of all main sets).
    3. This function does not rely on the design that all main sets have their set number as the last character of their names.
    """
    for main_set,rc_pairs in all_main_sets.items():
        if rc_pair in rc_pairs:
            return list(all_main_sets.keys()).index(main_set)
    return -1

def subset_of_rc_pair(rc_pair: tuple[float, int], all_subsets: dict[str, list[tuple[float, int]]]) -> int:
    """
    1. Return an 'int' that corrsponds to the subset number (1-indexed) that an (R,C) pair belongs to. In Reliability Design, the subset number corresponds to the amount of copies a device is being evaluated as. 
    2. Returns `-1` if the value is not found.
    3. Example:
        1. all_subsets = {'S^0_0': [(1, 0)], 'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}
        2. rc_pair = (0.99, 60)
        3. return: 2
            1. The pair (0.99, 60) is first matched with the subset S^1_2, and is the 2nd subset of S^1.
            2. The value corresponds to the amount of copies needed to obtain the (R,C) pair.
    4. This function relies on the design that the last character of a subset's name is the number of that subset.
        1. The function `subset_of_rc_pair_()` is a version that doesn't rely on this design.  
    """
    for subset,rc_pairs in all_subsets.items():
        if rc_pair in rc_pairs:
            return int(subset[-1])
    return -1

def subset_of_rc_pair_(rc_pair: tuple[float, int], all_main_sets: dict[str, dict[str, list[tuple[float, int]]]]) -> int:
    """
    1. Return an 'int' that corrsponds to the subset number (1-indexed) that an (R,C) pair belongs to. In Reliability Design, the subset number corresponds to the amount of copies a device is being evaluated as.
    2. Returns `-1` if the value is not found.
    3. Example:
        1. all_main_sets = {'S^0': [(1, 0)], 'S^1': [(0.9, 30), (0.99, 60)], 'S^2': [(0.72, 45), (0.864, 60), (0.8928, 75)]}
        2. rc_pair = (0.99, 60)
        3. return: 2
            1. The pair (0.99, 60) is first matched with the subset S^1_2, and is the 2nd subset of S^1.
            2. The value corresponds to the amount of copies needed to obtain the (R,C) pair.
    4. This version takes in `all_main_sets` as input unlike `subset_of_rc_pair()`.
    """
    for rc_pairs in all_main_sets.values():
        if rc_pair in rc_pairs:
            return rc_pairs.index(rc_pair) + 1
    return -1

def find_rc_pair_index_in_all_subsets(rc_pair: tuple[float, int], all_subsets:dict[str, list[tuple[float, int]]]) -> int:
    """
    1. Return the index number of an (R,C) pair in its subset group.
    2. Returns `-1` if the value is not found.
    TODO
    """
    for subset, rc_pairs in all_subsets.items():
        if rc_pair in rc_pairs:
            return all_subsets[subset].index(rc_pair)
        
    return -1
          
def subsets_under_nth_main_set(n: int, all_sets: dict[str, dict[str, list[tuple[float, int]]]]) -> dict[str, list[tuple[float, int]]]:
        """
        1. Return a dict corresponding to the subsets under a given main set.
        2. Main set is 0-indexed.
        3. Empty dict is returned if index is out of range.
        """
        try:
            main_set = list(all_sets.keys())[n]
        except IndexError:
            return {}
        return all_sets[main_set]

def len_args_not_equal_to_num(*args, num: int) -> bool:
    checker = []
    arg = None
    try:
        for arg in args:
            checker+=[len(arg) != num]
    except TypeError:
        raise TypeError(f"len() cannot be applied to {type(arg)} {arg}.")
    else:
        return any(checker)

def convert_input_to_list_of_ints(text: str, sep: str = " ") -> list[int]:
    s = input(text)
    try:
        l = [int(i) for i in s.split(sep=sep)]
    except ValueError:
        raise ValueError(f"Entered value cannot convert to 'int' type: {s}")
    else:
        return l
    
def convert_input_to_list_of_floats(text: str, sep: str = " ") -> list[float]:
    s = input(text)
    try:
        l = [float(i) for i in s.split(sep=sep)]
    except ValueError:
        raise ValueError(f"Entered value cannot convert to `float` type: {s}")
    else:
        return l
    
def convert_input_to_int(text: str) -> int:
    s = input(text)
    try:
        i = int(s)
    except ValueError:
        raise ValueError(f"Entered value cannot convert to 'int' type: {s}")
    else:
        return i

def len_args_equal_to_len_comp(*args, comp: Any) -> bool:
    for arg in args:
        if len(arg) != len(comp):
            raise ValueError(f"Length of {arg} must match length of {comp}.")
    return True

if __name__ == "__main__":
    COLUMNS = 4
    HEADER_COLS = ["D_i","C_i","r_i","u_i"]
    ROUND_N_PLACES = 4
    STARTING_SET = {"S^0": {"S^0_0": [(1,0)]} }
    main()