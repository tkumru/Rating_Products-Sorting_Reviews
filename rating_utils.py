import pandas as pd

def time_based_weighted_avg(df: pd.DataFrame, col_name: str, date_col: str,
                            w1: int=28, w2: int=26, 
                            w3: int=24, w4: int=22) -> float:
    """
    Function calculates mean of dataframe rating. Mean that is weighted
    for time values.

    Parameters
    ----------
    df : pd.DataFrame
    col_name : str
        Rating column name.
    w1 : int, optional
        Max weight. The default is 28.
    w2 : int, optional
        Second weighy. The default is 26.
    w3 : int, optional
        Third weight. The default is 24.
    w4 : int, optional
        Last weight. The default is 22.
    w4 : int, optional
        Last weight. The default is 22.
    date_col : str, optional
        Datetime column name.

    Returns
    -------
    float
        Dataframe rating time weighted mean.

    """
    count = df["days"].quantile([.2, .4, .6]).tolist()
    
    first_period = df.loc[df["days"] <= count[0], col_name].mean() * w1 / 100
    second_period = df.loc[(df["days"] > count[0]) & (df["days"] <= count[1]), col_name].mean() * w2 / 100
    third_period = df.loc[(df["days"] > count[1]) & (df["days"] <= count[2]), col_name].mean() * w3 / 100
    fourth_period = df.loc[(df["days"] > count[2]), col_name].mean() * w4 / 100
    
    first_date = str(df.loc[df["days"] <= count[0], date_col].max()).split(" ")[0]
    second_date = str(df.loc[(df["days"] > count[0]) & (df["days"] <= count[1]), date_col].max()).split(" ")[0]
    third_date = str(df.loc[(df["days"] > count[2]), date_col].min()).split(" ")[0] 
    
    print(f"First Period (After): {first_date} -> {w1} %, Rating Mean: {first_period}")
    print(f"Second Period (Between): {first_date} - {second_date} -> {w2} %, Rating Mean: {second_period}")
    print(f"Third Period (Between): {second_date} - {third_date} -> {w3} %, Rating Mean: {third_period}")
    print(f"Fourth Period (Before): {third_date} -> {w4} %, Rating Mean: {fourth_period}")
    
    return (first_period + second_period + third_period + fourth_period)
