# Data Card: NASDAQ Stock Price Dataset

## TEAM: 
Pelayo Negueruela 48308-ex
Aitana Lasheras 48277-ex
Ivan Madrid 48284-ex


## 1. Source of Data
This dataset was collected using the Yahoo Finance API through the `yfinance` Python library in Python.

The dataset contains daily stock price data for five NASDAQ-listed companies:
- Netflix (NFLX)
- Tesla (TSLA)
- PayPal (PYPL)
- Alphabet / Google (GOOGL)
- Adobe (ADBE)

Each company was downloaded using a different time period:
- NFLX: 1 month
- TSLA: 3 months
- PYPL: 6 months
- GOOGL: year-to-date
- ADBE: 1 year

The dataset includes these variables:
- Date
- Open
- High
- Low
- Close
- Volume
- Ticker
- Period

## 2. Descriptive Overview
The final dataset contains 541 rows and 8 columns.

There are no missing values in the dataset, which is a good sign of quality and completeness.

We used descriptive statistics to summarize the main numerical variables such as Close, High, Low, Open, and Volume. We also created basic visualizations to better understand the data.

The visualizations include:
- line charts showing the closing price over time for each company
- a bar chart comparing the average closing price by company
- a bar chart comparing the average trading volume by company

From the analysis, Tesla has the highest average closing price, while PayPal has the lowest. In terms of trading activity, Tesla and Netflix show higher average volume, while Adobe has the lowest volume among the selected companies.

## 3. KPI Results
- Completeness: 100.00%
- Latency: 0 day(s)
- Accuracy: 100.00%
- Consistency: 100.00%

## 4. KPI Explanation
**Completeness** checks whether the dataset has missing values. In this case, there were no missing values, so completeness is 100%.

**Latency** checks how up to date the dataset is by comparing the most recent date in the dataset with the current date. In this case, the latency is 0 days.

**Accuracy** was evaluated using internal checks in the dataset. For example, we checked that:
- High is greater than or equal to Low
- Open is between Low and High
- Close is between Low and High
- Volume is not negative

All of these checks were correct, so the accuracy result is 100%.

**Consistency** checks whether the dataset has a stable structure, correct data types, and no duplicate records for the same Date and Ticker. All of these checks were correct, so consistency is 100%.

## 5. Conclusion
Overall, the dataset has strong quality for basic financial analysis.

It is complete, up to date, accurate according to the internal validation rules, and consistent in structure. The descriptive statistics and the charts also show clear differences between the selected companies in terms of stock price and trading activity.

For this reason, I consider the dataset suitable for a simple financial analysis and for demonstrating data quality KPIs.