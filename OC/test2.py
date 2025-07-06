def remove_bpairs_from_d(d: dict[str, list[tuple[float, int]]], bad_pairs: list[tuple[float, int]]):
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

d = {'S^3_1': [(0.36, 65), (0.432, 80), (0.4464, 95)], 'S^3_2': [(0.54, 85), (0.648, 100)]}
bad_pairs = [(0.4464, 95)]
print(remove_bpairs_from_d(d, bad_pairs))