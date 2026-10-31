"""Rental market analysis: clean the data, load it into SQLite, run the SQL queries, and make charts.

Setup:
    pip install pandas matplotlib
    Download House_Rent_Dataset.csv from Kaggle (iamsouravbanerjee/house-rent-prediction-dataset)
    and put it in this folder.
Run:
    python analysis.py
"""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

CSV_FILE = "House_Rent_Dataset.csv"
DB_FILE = "rental.db"
CHART_DIR = Path("charts")
CHART_DIR.mkdir(exist_ok=True)

# ---------- 1. Load and inspect ----------
df = pd.read_csv(CSV_FILE)
print("Rows, columns:", df.shape)
print("\nMissing values per column:\n", df.isnull().sum())

# ---------- 2. Clean ----------
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
before = len(df)
df = df.drop_duplicates()
df = df[(df["rent"] > 0) & (df["size"] > 0)].copy()
df["rent_per_sqft"] = (df["rent"] / df["size"]).round(2)
print(f"\nRows kept after cleaning: {len(df)} of {before}")

# Extreme rents can distort averages. Check them yourself before deciding what to do.
print("\nRent summary:\n", df["rent"].describe())
print("\n5 highest rents:\n", df.nlargest(5, "rent")[["city", "bhk", "size", "rent"]])

# ---------- 3. Load into SQLite ----------
regions = pd.DataFrame(
    {
        "city": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata"],
        "region": ["West", "North", "South", "South", "South", "East"],
    }
)
with sqlite3.connect(DB_FILE) as conn:
    df.to_sql("listings", conn, if_exists="replace", index=False)
    regions.to_sql("regions", conn, if_exists="replace", index=False)

    # ---------- 4. Run the SQL file, one query at a time ----------
    queries = [
        q.strip() for q in Path("queries.sql").read_text().split(";") if q.strip()
    ]
    results = []
    for i, q in enumerate(queries, start=1):
        out = pd.read_sql_query(q, conn)
        results.append(out)
        print(f"\n--- Query {i} ---\n{out.to_string(index=False)}")

# ---------- 5. Charts ----------
avg_city = results[0]
ax = avg_city.plot(kind="bar", x="city", y="avg_rent", legend=False, figsize=(7, 4))
ax.set_title("Average monthly rent by city")
ax.set_ylabel("Rent (INR)")
plt.tight_layout()
plt.savefig(CHART_DIR / "avg_rent_by_city.png")
plt.close()

per_sqft = results[2]
ax = per_sqft.plot(
    kind="bar", x="city", y="avg_rent_per_sqft", legend=False, figsize=(7, 4)
)
ax.set_title("Average rent per sq ft by city")
ax.set_ylabel("INR per sq ft")
plt.tight_layout()
plt.savefig(CHART_DIR / "rent_per_sqft_by_city.png")
plt.close()

furn = results[3].pivot(index="city", columns="furnishing_status", values="avg_rent")
ax = furn.plot(kind="bar", figsize=(8, 4))
ax.set_title("Average rent by furnishing status")
ax.set_ylabel("Rent (INR)")
plt.tight_layout()
plt.savefig(CHART_DIR / "rent_by_furnishing.png")
plt.close()

# Median is more reliable than the mean when a few listings are very expensive.
print(
    "\nMedian rent by city (pandas):\n",
    df.groupby("city")["rent"].median().sort_values(),
)
print("\nDone. Charts are in the 'charts' folder.")
