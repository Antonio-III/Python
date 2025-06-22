import pandas as pd
"""
Calculates the Cohen's d using data from control group and experiment groups. Both files must be csv files.
"""
def main(c:dict,e:dict)->None:
    """
    1. Prints Cohen's d (effect size) using data from Control and Experiment. Only usable if this module is directly run.
        1. See most bottom line of the module to see what the values are. 
    """

    mean=[0,c["mean"],e["mean"]]
    std=[0,c["std"],e["std"]]
    pooled_std=pooled_std_for_cohen_d(std)

    effect_size=calculate_cohens_d(mean,pooled_std)
    print(f"Effect size: {effect_size}")

    return None

def pooled_std_for_cohen_d(std:list)->float:
    """
    1. Returns the pooled standard deviation of 2 groups.
    """
    return ((std[1]**2+std[2]**2)/2)**0.5
    
def pooled_std_for_cohen_d_alt(std:list,n:tuple)->float:
        """
        1. Returns the pooled standard deviation of 2 groups using an alternative formula. 
        """
        numerator=(n[1]-1)*(std[1]**2)+(n[2]-1)*(std[2]**2)
        denominator=n[1]+n[2]-2

        return (numerator/denominator)**0.5

def calculate_cohens_d(mean:list,pooled_std:float):
    """
    1. Effect size interpretation, though you should not be the standard for all contexts.
        1. Very small = 0.01
        1. Small = 0.2.
        2. Medium = 0.5.
        3. Large = 0.8.
        4. Very large = 1.2.
        5. Huge = 2.
    """
    return (abs(mean[1]-mean[2]))/pooled_std


if __name__=="__main__":
    SCORE="Score"
    CONTROL_GROUP_DIR=rf"{input('Enter path of the the control group dataset.')}"
    EXPERIMENTAL_GROUP_DIR=rf"{input('Enter path of the the experimental group dataset.')}"
    # Checks if the dataset is just an empty. Error catching needs to be improved.
    if not CONTROL_GROUP_DIR and not EXPERIMENTAL_GROUP_DIR:
        raise ValueError("Not valid directory.")
    C=pd.read_csv(CONTROL_GROUP_DIR)
    E=pd.read_csv(EXPERIMENTAL_GROUP_DIR)
    c={"n":len(C.index),"mean":C[SCORE].mean(),"std":C[SCORE].std()}
    e={"n":len(E.index),"mean":E[SCORE].mean(),"std":E[SCORE].std()}
    c_stats=f"Control: {c["n"]}, Mean: {c["mean"]}, STD: {c["std"]}."
    e_stats=f"Experimental: {e["n"]}, Mean: {e["mean"]}, STD: {e["std"]}."
    print(f"{c_stats}\n{e_stats}")
    main(c,e)
