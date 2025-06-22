"""
This script does all the Machine Learning steps and outputs the results to the user. The only requirement is that the user input a valid PATH to the dataset.
"""
CODEGUARDIAN_LINK = "https://pond-biplane-31b.notion.site/1a963cb190b680fc8999c903632da8d1"

# Options. Change as needed.
HIST_SIZE = (20,13)
HEATMAP_SETTINGS = {"annot": True, "cmap": "Blues"}
FIG_SIZE = (15,8)

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# You can add supported models here. Make sure they are imported
SUPPORTED_MODELS= {"LinearRegression": LinearRegression(),
                   "KNeighborsClassifier": KNeighborsClassifier(),
                   "DecisionTreeClassifier": DecisionTreeClassifier()}

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

# Metrics for KNeighbors Classifier
from sklearn.metrics import accuracy_score, classification_report 

# Metrics for LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.feature_extraction.text import CountVectorizer

import random 

from sklearn.base import BaseEstimator

from typing import cast
from scipy.sparse import csr_matrix

# Do not change
MAX_SEED = 2**32- 1
MIN_SEED = 0

NO_SEED_INPUT= -1

FIRST_RESULT = "Classification Result"

CLASSIFICATION_RESULT_TEMPLATE = "Accuracy score: {accuracy_sc}\nClassification Report: {classification_re}"
R_SQ_TEMPLATE = "Mean Squared Error: {mean_sq_err}\nMean Absolute Error: {mean_abs_err}\nR Squared Score: {rsq_sc}"

TEXT_CONVERSION_MESSAGE = "Text conversion using {} done."

# Model function
def model_predict(dataset: str,
                  dependent_var: str,
                  str_in_data: bool,
                  str_columns_dum: list,
                  str_columns_cvector: list,
                  random_state: int,
                  test_size: float,
                  model_used: BaseEstimator,
                 ) -> tuple:  
    
    # 1.2 Loading dataset.
    print("Loading dataset...")

    df = load_dataset(dataset_dir=dataset)

    # Since we are outputting the head before this (model_predict) is called, the code directly below has been ommitted.
    # print(f"Dataset head:\n{df.head()}")
    print("Dataset loading complete.")

    # 2. Data cleaning/preprocessing.
    print("Starting data preprocessing...")
    
    X,y = data_preprocessing(df=df, dependent_var=dependent_var,str_in_data=str_in_data, str_columns_dum=str_columns_dum, str_columns_cvector=str_columns_cvector)

    print(f"Features (X):\n{X.head()}")
    print(f"Features (y):\n{y.head()}")
    
    print("Data cleaning complete.")

    # Visualization
    if not str_in_data:
        print(df.head())
        visualize_data(df=df)

    # 3. Data splitting
    print("Starting data splitting...")
    
    X_train, X_test, y_train, y_test = data_splitting(X, y, test_size=test_size, random_state=random_state)

    print(f"Training set size: {X_train.shape[0]}.")
    print(f"Test set size:{X_test.shape[0]}.")
    print("Data splitting complete.")

    # 4. Model training.
    print("Starting model training...")

    model = model_training(model_used=model_used, 
    X_train=X_train, y_train=y_train)

    print("Model training complete.")

    # 5. Model testing.
    print("Starting model training...")

    y_pred = model_testing(model=model, X_test=X_test)
    
    print("Model testing complete.")

    # 6. Model evaluation.
    print("Starting model evaluation...")

    output = model_evalution(y_test=y_test, y_pred=y_pred)

    print("Model evaluation complete.")
    return output
    
def load_dataset(dataset_dir: str) -> pd.DataFrame:
    """
    Step 1 of 6 of the Machine Learning steps. This functions returns a DataFrame object, which can be used in the next step.
    """
    return pd.read_csv(fr"{dataset_dir}")

def visualize_data(df: pd.DataFrame) -> None:
    """
    Visualizes data. sns.heatmap, pd.DataFrame.hist, and plt.Figure functions are used.
    """
    heatmap_settings = HEATMAP_SETTINGS
    hist_settings = HIST_SIZE
    figure_settings = FIG_SIZE

    print(sns.heatmap(data=df.corr(), **heatmap_settings))

    df.hist(figsize=hist_settings)
        
    plt.figure(figsize=figure_settings)

    return None

def data_preprocessing(df: pd.DataFrame, dependent_var: str, str_in_data: bool, str_columns_dum: list, str_columns_cvector: list) -> tuple[pd.DataFrame, pd.DataFrame | pd.Series]:
    """
    Step 2 of 6 of the Machine Learning steps. Converts textual columns to numerical data. Returns 2 objects: The independent variable (X) and the dependent variable (y).
    """
    if str_in_data:
        # Doing this should be okay since the column that was passed to 'dum' should not be the same column that is passed to 'cvector'.
        df = convert_text_col_to_num_dum(df=df, str_columns=str_columns_dum) 
        df = convert_text_col_to_num_cvector(df=df, str_columns=str_columns_cvector) 
    
    X = df.drop(columns=[col for col in df.columns if col.startswith(dependent_var)], axis=1)
    y = df[[col for col in df.columns if col.startswith(dependent_var)]]

    return X, y

def convert_text_col_to_num_le(df: pd.DataFrame, str_columns: list) -> pd.DataFrame:
    """
    Converts the DataFrame's texts into numerical data. Uses LabelEncoder. DO NOT USE IF MODEL IS SENSITIVE TO NUMERIC DISTANCE (linear models, KNN, tree-based models, etc.).
    """
    for str_column in str_columns:
        le = LabelEncoder()
        df[str_column] = le.fit_transform(df[str_column])

    print(TEXT_CONVERSION_MESSAGE.format("LabelEncoder"))

    return df

def convert_text_col_to_num_dum(df: pd.DataFrame, str_columns: list) -> pd.DataFrame:
    """
    Converts the DataFrame's texts into numerical data. Uses pd.get_dummies. Recommended for DataFrame columns with categorical values.
    """

    df = pd.get_dummies(data=df, columns=str_columns)

    # User and debugging feedback.
    print(f"Column names are now: {df.columns}")
    print(TEXT_CONVERSION_MESSAGE.format("pd.get_dummies"))
     
    
    return df

def convert_text_col_to_num_cvector(df: pd.DataFrame, str_columns: list) -> pd.DataFrame:
    """
    Converts the DataFrame's texts into numerical data. Returns combined DataFrame of all transformed columns. 
    
    Uses CountVectorizer. Use for text classification problems like datasets containing messages, reviews, documents, etc.. Recommended for DataFrame columns with free-form texts.
    """
    vectorized_data = []
    
    for column in str_columns:
        vectorizer = CountVectorizer()
        transformed = cast(csr_matrix, vectorizer.fit_transform(df[column].fillna("")))
        
        col_names = [f"{column}_{word}" for word in vectorizer.get_feature_names_out()]
        
        transformed_df = pd.DataFrame(transformed.toarray(), columns=col_names, index=df.index)
        
        vectorized_data.append(transformed_df)

    vectorized_cols = df.drop(columns=str_columns)

    df = pd.concat([vectorized_cols] + vectorized_data, axis=1)

    print(TEXT_CONVERSION_MESSAGE.format("CountVectorizer"))
  
    return df

def data_splitting(X: pd.DataFrame, y: pd.DataFrame | pd.Series, test_size: float, random_state: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Step 3 of 6 of the Machine Learning steps. Splits the independent and dependent variables into 2 categories: Training, and Testing.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return X_train, X_test, y_train, y_test


def model_training(model_used: BaseEstimator, X_train: pd.DataFrame, y_train: pd.Series) -> BaseEstimator:
    """
    Step 4 of 6 of the Machine Learning steps. Trains the model with the given training dataset. Returns the trained Model.
    """
    model = model_used

    model.fit(X_train, y_train) # type: ignore
    return model

def model_testing(model: BaseEstimator, X_test: pd.DataFrame) -> np.ndarray:
    """
    Step 5 of 6 of the Machine Learning steps. Tests the model with the given training dataset. Returns the prediction.
    """
    y_pred = model.predict(X_test) # type: ignore
    return y_pred

def model_evalution(y_test: pd.Series, y_pred: np.ndarray) -> tuple:
    """
    Step 6 of 6 of the Machine Learning steps. Evaluates the model by comparing the Model's prediction with the actual dataset's values. Returns the result in a string. 
    """ 
    results = {"Classification Result": "", "Regression Result": ""}
    
    for result in results.keys():
        try:
            if result == FIRST_RESULT:
                results[result] = CLASSIFICATION_RESULT_TEMPLATE.format(
                    accuracy_sc = accuracy_score(y_test, y_pred), 
                    classification_re = classification_report(y_test, y_pred)
                    )
            else: # Regression
                results[result] = R_SQ_TEMPLATE.format(
                    mean_sq_err = mean_squared_error(y_test, y_pred), 
                    mean_abs_err = mean_absolute_error(y_test, y_pred), 
                    rsq_sc = r2_score(y_test, y_pred)
                    )
        except Exception:
            results[result] = f"{result}: N/A"
    return tuple(results.values())  

def set_random_state(seed: str) -> int:
    """
    Returns an int object to be used as the value for the random_state variable. The function checks if the inputted seed is a number, and must be at least 0. 
    """
    random_state = 0
    try:
        seed_int = int(seed)
    except ValueError:
        random_state = generate_random_seed()
    else:
        random_state = seed_int if seed_int >= MIN_SEED and seed_int <= MAX_SEED else generate_random_seed(ommit_error=True)
    finally:
        return random_state 

def generate_random_seed(ommit_error: bool = False) -> int:
    """
    In the case of errors in setting the seed, a random seed is returned instead.
    """
    if not ommit_error:
        print(f"Entered seed does not meet numbers in the range({MIN_SEED}~{MAX_SEED}). Using random seed instead.")

    random_state = random.randrange(MAX_SEED)
    return random_state

def script_intro() -> bool:
    """
    Intro for the script. Gives the user a choice to continue or exit the script.
    """
    intro_s_form_or_not = ("s", "are") if len(SUPPORTED_MODELS)>=2 else ("", "is")
    
    print("Supported model{} in the script {}: ".format(*intro_s_form_or_not), end = "")
    
    for model in SUPPORTED_MODELS:
        print(f"{model} ", end = "")
    
    print(end="\n")
    try:
        input("Press any key to continue continue. Press Ctrl+c twice to exit:\n")
    except (KeyboardInterrupt, EOFError):
        print("Program exit.")
        return False
    else:
        return True
    
def main() -> None:
    """
    This script goes through all the Machine Learning steps and outputs its classification and regression score. The script iterates through multiple Models to get their corresponding results. This means that whatever values are in global SUPPORTED_MODELS, those are the Models whose classification and regression score will be outputted at the end of the program.
    """
    if script_intro():
            persistent_values = set_script_variables()
            for value in persistent_values:
                print(value)

            final_results = {}

            for model in SUPPORTED_MODELS.keys():

                print(f"Using Model: {model}.")
                model_used = SUPPORTED_MODELS[model]

                final_results[model] = model_predict(*persistent_values, model_used=model_used)

            for model in final_results.keys():
                print(f"Using {model}, its results are:")
                for result in final_results[model]:
                    print(result)

            print("Results finished.")

            print(f"Visit {CODEGUARDIAN_LINK} for more programs.")

            print("Program exit.")

def set_script_variables() -> tuple:
    """
    Set the variables that will be used throughout the function `get_outcome`.
    """
    dataset_dir = input("Enter dataset path including the dataset file itself. Path must be in your computer directory:\n").strip('"').strip("'")

    # Let the user see the column names
    df = load_dataset(dataset_dir=dataset_dir)
    print(f"Dataset Columns. Remember the column names:\n: {df.head()}")
    
    dependent_var = input("Enter dependent variable (i.e. the column name of the variable you want to predict values of, case-sensitive):\n")

    str_in_data = input("Are there textual data in the dataset (y/n)?\n").lower().startswith("y") 

    str_columns_dum = []
    str_columns_cvector = []

    if str_in_data:
        str_columns_dum = set_str_columns(algorithm="dum")            
        str_columns_cvector = set_str_columns(algorithm="cvector") 
    
    
    seed = input(f"Enter seed (Enter {NO_SEED_INPUT} to auto generate seed). Valid seeds must be at least {MIN_SEED}:\n")

    random_state = set_random_state(seed)

    test_size = int(input("Enter the train/test split for TEST size (E.g. 30 if 70% training and 30% test):\n"))/100

    return dataset_dir, dependent_var, str_in_data, str_columns_dum, str_columns_cvector, random_state, test_size

def set_str_columns(algorithm: str) -> list:
    """
    Sets str_columns variable with their given pre-written description that makes them distinct from each other.
    """
    prompt = "Enter column names (case-sensitive) that have textual values, separated by a whitespace that {algorithm}:\n"

    algorithms_desc = {
        "cvector": "are non-categorical (columns that contain free-form text like messages, reviews, documents, etc.)",

        "dum": "are categorical (columns that have values like red/blue/green; yes/no; high/low, etc.)"
        }
    
    return input(prompt.format(algorithm=algorithms_desc[algorithm])).split()
       
if __name__ == "__main__":
    main()