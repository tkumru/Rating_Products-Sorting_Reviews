import pandas as pd
from rating_utils import time_based_weighted_avg
from comment_utils import score_pos_neg_diff, score_average_rating, \
    wilson_lower_bound

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 500)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.float_format", lambda x: '%.5f' % x)

"""
reviewerID: User ID
asin: Product ID
reviewerName: User name
helpful: Helpful comment
reviewText: Comment
overall: Product rating
summary: Comment summary
unixReviewTime: Comment time
reviewTime: Comment time raw
day_diff: Day of passed comment time
helpful_yes: Comment up count
total_vote: Total comment rating count
"""

df = pd.read_csv("dataset/amazon_review.csv")
df.head()

df.dtypes
df.describe().T
df.info()

df.isnull().sum()
df.dropna(inplace=True)

####################
# Average
####################

df["overall"].mean()

####################
# Time-Based Weighted Average
####################

df["reviewTime"] = pd.to_datetime(df["reviewTime"]) # 2014-12-07
df["reviewTime"].max()

analyze_date = pd.to_datetime("2014-12-09 00:00:00")

df["days"] = (analyze_date - df["reviewTime"]).dt.days

time_based_weighted_avg(df, "overall", "reviewTime")

###################################################
# Up-Down Diff Score = (up ratings) − (down ratings)
###################################################

df[["total_vote", "helpful_yes"]].head(10)

df["helpful_no"] = df["total_vote"] - df["helpful_yes"]

df = score_pos_neg_diff(df, "helpful_yes", "helpful_no")

###################################################
# Score Average rating = (up ratings) / (all ratings)
###################################################

df = score_average_rating(df, "helpful_yes", "helpful_no")

###################################################
# Wilson Lower Bound Score
###################################################

df = wilson_lower_bound(df, "helpful_yes", "helpful_no")

df[["reviewerID", "overall", "score_pos_neg_diff", 
    "score_average_rating", "wilson_lower_bound"]] \
    .sort_values("wilson_lower_bound", ascending=False).head(20)
