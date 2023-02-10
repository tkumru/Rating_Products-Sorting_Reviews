import pandas as pd
import scipy.stats as st
import numpy as np

def score_pos_neg_diff(df: pd.DataFrame, 
                       up_col_name: str,
                       down_col_name: str) -> pd.DataFrame:
    """
    Function generates scores for comments. Function gets difference 
    between positive up score and negative down score.

    Parameters
    ----------
    df : pd.DataFrame
    up_col_name : str
        Up score column name.
    down_col_name : str
        Down score column name.

    Returns
    -------
    df : pd.DataFrame
        Dataframe is added score_pos_neg_diff column.

    """
    df["score_pos_neg_diff"] = df[up_col_name] - df[down_col_name]
    
    return df

def score_average_rating(df: pd.DataFrame,
                         up_col_name: str,
                         down_col_name: str) -> pd.DataFrame:
    """
    Function generates average scores for comments. Function gets percent 
    on positive up score and negative down score.

    Parameters
    ----------
    df : pd.DataFrame
    up_col_name : str
        Up score column name.
    down_col_name : str
        Down score column name.

    Returns
    -------
    df : pd.DataFrame
        Dataframe is added score_average_rating column.

    """
    def calculate(up: int, down: int) -> float:
        return 0 if up + down == 0 else up / (up + down)
    
    df["score_average_rating"] = df.apply(lambda x: calculate(x[up_col_name], 
                                                             x[down_col_name]), 
                                          axis=1)
    
    return df

def wilson_lower_bound(df: pd.DataFrame,
                       up_col_name: str,
                       down_col_name: str) -> pd.DataFrame:
    """
    Function calculates Wilson Lower Bound for all column values.

    Parameters
    ----------
    df : pd.DataFrame
    up_col_name : str
        Up score column name.
    down_col_name : str
        Down score column name.

    Returns
    -------
    df : pd.DataFrame
        Dataframe is added wilson_lower_bound column.

    """
    def calculte(up: int,
                 down:int,
                 confidence: float=0.95) -> float:
        """
        Function calculates Wilson Lower Bound. This bound is used for 
        bernoulli parameter. It is for sorting.

        Parameters
        ----------
        up : int
            Up count.
        down : int
            Down count.
        confidence : float, optional
            Confidence. The default is 0.95.

        Returns
        -------
        float
            Rating.
            
        Example
        -------
        If scores are between 1 - 5, 1 - 3 will be negative, 4 - 5 will be
        positive for usable for bernoully therefore it should calculate
        bayesian average rating.

        """
        n = up + down
        if n == 0:
            return 0
        z = st.norm.ppf(1 - (1 - confidence) / 2)
        phat = 1.0 * up / n
        return (phat + z * z / (2 * n) - z * 
                np.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)
    
    df["wilson_lower_bound"] = df.apply(lambda x: calculte(x[up_col_name], 
                                                           x[down_col_name]),
                                        axis=1)
    
    return df
