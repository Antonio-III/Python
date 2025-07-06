"""
Calculates the Cohen's d using data from control group and experiment groups. Both datasets must be csv files.

Table of Contents
    main
    pooled_std
    pooled_std_alt
    calculate_cohens_d
    pooled_std_alt2
    pooled_std_alt2_simplified
"""

import pandas as pd

def main(c: dict, e: dict) -> None:
    """
    1. Prints Cohen's d (effect size) using data from Control and Experiment. Only usable if this module is directly run.
        1. See most bottom line of the module to see what the values are. 
    """

    mean = [0, c['mean'], e['mean']]
    std = [0, c['std'], e['std']]
    sd_pooled = pooled_std(std[1], std[2])

    effect_size = calculate_cohens_d(mean, sd_pooled)
    print(f'Effect size: {effect_size}')

    return None

def pooled_std(sd_1: float, sd_2: float) -> float:
    """
    Returns the pooled standard deviation of 2 groups.
    
    SD_pooled = sqrt((SD_1^2 + SD_2^2)/2)

    Where:
        SD_1 = Standard deviation for group 1
        SD_2 = Standard deviation for group 2

    Source: https://www.statisticshowto.com/pooled-standard-deviation/
    """
    return ((sd_1**2 + sd_2**2)/2)**0.5
    
def pooled_std_alt(std: list, n: tuple) -> float:
        """
        Returns the pooled standard deviation of 2 groups using an alternative formula. 

        SD*_pooled = sqrt( ((n_1 - 1) * SD_1^2 + (n_2 - 1) * SD_2^2) / n_1 + n_2 - 2 )

        Where:
            n_1 = Sample size of group 1
            n_2 = sample size of group 2

        Source: https://www.statisticshowto.com/pooled-standard-deviation/
        """
        numerator = (n[1] - 1 ) * (std[1]**2) + (n[2] - 1) * (std[2]**2)
        denominator = n[1] + n[2] - 2

        return (numerator/denominator)**0.5

def calculate_cohens_d(mean: list, pooled_std: float) -> float:
    """
    Effect size interpretation, though you should not be the standard for all contexts.
        1. Very small = 0.01
        1. Small = 0.2.
        2. Medium = 0.5.
        3. Large = 0.8.
        4. Very large = 1.2.
        5. Huge = 2.
    """
    return (abs(mean[1]-mean[2]))/pooled_std

def pooled_std_alt2(list_of_sample_sizes: list[int], list_of_std_deviations: list[float], k: int) -> float:
    """
    Calculate standard pool deviation if more than 2 groups.
    s_pooled = sqrt(((n_1 - 1) * s_1^2 + (n_2 - 1) * s_2^2 + ... + (n_k - 1) * s_k^2) / n_1 + n_2 + ... + n_k - k)

    Where:
        n_k = list_of_sample_sizes[i]
        s_k = list_of_std_deviations[i]
        k == len(list_of_sample_sizes) and k == len(list_of_std_deviations)
    
    Source: https://www.statisticshowto.com/pooled-standard-deviation/
    """
    numerator = sum([(list_of_sample_sizes[i] - 1) * list_of_std_deviations[i]**2 for i in range(k)])
    denominator = sum([list_of_sample_sizes[i] for i in range(k)])

    return (numerator/denominator)**0.5

def pooled_std_alt2_simplified(list_of_std_deviations: list[float], k: int) -> float:
    """
    Calculate standard pool deviation if more than 2 groups WITH EQUAL SAMPLE SIZES. 
    s_pooled = sqrt(s_1^2 + s_2^2 + ... + s_k^2 / k)

    Where:
        s_k = list_of_std_deviations[i]
        k = sample size
    
    Source: https://www.statisticshowto.com/pooled-standard-deviation/
    """
    numerator = sum([list_of_std_deviations[i]**2 for i in range(len(list_of_std_deviations))])
    denominator = k 

    return (numerator/denominator)**0.5
     
if __name__== '__main__':
    SCORE = input('Enter column name you are measuring.\n')
    CONTROL_GROUP_DIR = rf'{input("Enter path of the the control group dataset.\n")}'
    EXPERIMENTAL_GROUP_DIR = rf'{input("Enter path of the the experimental group dataset.\n")}'

    # Checks if the dataset is empty. 
    # Error catching needs to be improved.
    if not CONTROL_GROUP_DIR and not EXPERIMENTAL_GROUP_DIR:
        raise ValueError('Not valid directory.')
    
    C = pd.read_csv(CONTROL_GROUP_DIR)
    E = pd.read_csv(EXPERIMENTAL_GROUP_DIR)
    c = {'n': len(C.index), 'mean': C[SCORE].mean(), 'std': C[SCORE].std()}
    e = {'n': len(E.index), 'mean': E[SCORE].mean(), 'std': E[SCORE].std()}
    c_stats = f'Control: {c["n"]}, Mean: {c["mean"]}, STD: {c["std"]}'
    e_stats = f'Experimental: {e["n"]}, Mean: {e["mean"]}, STD: {e["std"]}'
    
    print(c_stats)
    print(e_stats)
    
    main(c, e)
