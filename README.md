# Rental Market Analysis (India)

## What it does
Analyses about 4,700 rental listings across six Indian cities to see how rent changes by city, size, number of bedrooms and furnishing. It cleans the data with pandas, loads it into SQLite, answers business questions with SQL (aggregations, a join and a window function), and produces charts.

## Data
House Rent Prediction Dataset on Kaggle by Sourav Banerjee (CC BY-SA 4.0):
https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset

## How to run
1. `pip install pandas matplotlib`
2. Download `House_Rent_Dataset.csv` from the Kaggle link and place it in this folder.
3. `python analysis.py`

Files: `analysis.py` (cleaning, loading, charts), `queries.sql` (the seven SQL queries), `charts/` (output images).

## Questions answered
1. Average rent and listing count by city
2. Average rent by city and bedrooms
3. Rent per square foot by city
4. Effect of furnishing status on rent
5. Top 3 most expensive localities in each city (window function)
6. Average rent by region (join)
7. Median rent by city (window function)

## Key findings
Mumbai has the highest average rent (about 85,300) and Kolkata the lowest (about 11,600). Averages sit well above medians in every city, for example Mumbai 85,321 against 52,000, because a few very expensive listings pull them up. The listing counts and average rents by city matched an independent pandas recalculation, and the Chennai figures also matched Google Sheets formulas.

## How I used AI
Tools: Claude helped me draft the SQL queries (aggregations, a window function and a join), the pandas cleaning script and a median query. I ran every query and checked the results myself.

## What the AI got wrong, and how I checked
The median query written with Claude's help was correct and matched my pandas medians for all six cities. SQLite has no built-in MEDIAN function, so the query uses ROW_NUMBER and COUNT window functions to find the middle rows. I verified the results with an independent pandas recalculation (check.py) and a Google Sheets pivot check, rather than trusting the generated query.

## Limitations
The data is a single snapshot from 2022 and covers only six cities. Listed rents are asking prices, not final rents, and a few extreme listings skew the averages, so medians are more reliable.

## License credit 
Data: House Rent Prediction Dataset by Sourav Banerjee on Kaggle (https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset). Please see the dataset page for its license terms.