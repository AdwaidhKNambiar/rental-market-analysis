"""Independent check: recompute key numbers straight from the CSV with pandas
and compare them with the SQL results stored in rental.db.
Run in the same folder as House_Rent_Dataset.csv and rental.db:  python check.py
"""

import sqlite3

import pandas as pd

raw = pd.read_csv("House_Rent_Dataset.csv")
print("Raw rows in CSV:", len(raw))

# 1. Average rent by city, straight from the raw CSV (no cleaning script involved)
pandas_avg = raw.groupby("City")["Rent"].agg(["count", "mean", "median"]).round(0)
print("\nFrom pandas on the raw CSV:\n", pandas_avg)

# 2. The same thing from the SQL table built by analysis.py
with sqlite3.connect("rental.db") as conn:
    sql_avg = pd.read_sql_query(
        "SELECT city, COUNT(*) AS listings, ROUND(AVG(rent), 0) AS avg_rent "
        "FROM listings GROUP BY city ORDER BY city",
        conn,
    )
print("\nFrom SQL (rental.db):\n", sql_avg.to_string(index=False))

# 3. Compare. Differences mean duplicates or invalid rows were removed, or something is wrong.
merged = pandas_avg.reset_index().merge(sql_avg, left_on="City", right_on="city")
merged["listing_diff"] = merged["count"] - merged["listings"]
merged["avg_diff"] = (merged["mean"] - merged["avg_rent"]).round(0)
print(
    "\nComparison:\n",
    merged[
        ["City", "count", "listings", "listing_diff", "mean", "avg_rent", "avg_diff"]
    ].to_string(index=False),
)
print(
    "\nIf listing_diff is 0 and avg_diff is 0 for every city, the SQL matches the raw data."
)
print("If not, find out why: duplicates removed by analysis.py, or a real mistake.")
