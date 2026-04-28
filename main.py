import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# I chose 5 NASDAQ companies and used a different period for each one,
# because that was one of the requirements of the assignment.
companies = {
    "NFLX": "1mo",
    "TSLA": "3mo",
    "PYPL": "6mo",
    "GOOGL": "ytd",
    "ADBE": "1y"
}

# I will store each company's data here and then combine everything at the end.
frames = []

for ticker, period in companies.items():
    # Download daily stock price data from Yahoo Finance
    data = yf.download(ticker, period=period, interval="1d")

    # yfinance sometimes creates multi-level columns, so I simplify them
    data.columns = data.columns.get_level_values(0)

    # I reset the index so that Date becomes a normal column
    data = data.reset_index()

    # I add the company ticker and the selected period to each row
    # so later I know where each observation comes from
    data["Ticker"] = ticker
    data["Period"] = period

    # Save this company's table
    frames.append(data)

# Combine all company tables into one final dataset
dataset = pd.concat(frames, ignore_index=True)

# Remove the column group name to make the output cleaner
dataset.columns.name = None

# --------------------
# Basic dataset checks
# --------------------

print("Dataset shape:")
print(dataset.shape)

print("\nMissing values:")
print(dataset.isnull().sum())

print("\nOverall descriptive statistics:")
print(dataset[["Close", "High", "Low", "Open", "Volume"]].describe())

# Here I print descriptive statistics for each company separately.
# This helps me compare their price levels and trading volume.
for ticker in dataset["Ticker"].unique():
    print(f"\nDescriptive statistics for {ticker}:")
    company_data = dataset[dataset["Ticker"] == ticker]
    print(company_data[["Close", "High", "Low", "Open", "Volume"]].describe())

# --------------------
# Basic visualizations
# --------------------

# 1) Line chart for each company
# I use these charts to see how the closing price changed over time.
for ticker in dataset["Ticker"].unique():
    company_data = dataset[dataset["Ticker"] == ticker]

    plt.figure(figsize=(8, 4))
    plt.plot(company_data["Date"], company_data["Close"])
    plt.title(f"{ticker} Close Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 2) Bar chart of average closing price
# This makes it easier to compare companies in one single figure.
avg_close = dataset.groupby("Ticker")["Close"].mean()

plt.figure(figsize=(8, 4))
avg_close.plot(kind="bar")
plt.title("Average Close Price by Company")
plt.xlabel("Ticker")
plt.ylabel("Average Close Price")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 3) Bar chart of average volume
# I use this chart to compare trading activity between companies.
avg_volume = dataset.groupby("Ticker")["Volume"].mean()

plt.figure(figsize=(8, 4))
avg_volume.plot(kind="bar")
plt.title("Average Volume by Company")
plt.xlabel("Ticker")
plt.ylabel("Average Volume")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# --------------------
# KPI calculations
# --------------------

# 1. Completeness
# This checks if there are missing values in the dataset.
total_cells = dataset.shape[0] * dataset.shape[1]
missing_cells = dataset.isnull().sum().sum()
completeness = ((total_cells - missing_cells) / total_cells) * 100

# 2. Latency
# This checks how recent the dataset is.
# I compare the latest date in the dataset with today's date.
dataset["Date"] = pd.to_datetime(dataset["Date"])
latest_date = dataset["Date"].max().normalize()
today = pd.Timestamp.today().normalize()
latency_days = (today - latest_date).days

# 3. Accuracy
# Since I do not have another external source to compare prices,
# I check internal logic rules in the dataset.
# For example:
# - High should be >= Low
# - Open should be between Low and High
# - Close should be between Low and High
# - Volume should not be negative
valid_high_low = (dataset["High"] >= dataset["Low"]).all()
valid_open = ((dataset["Open"] >= dataset["Low"]) & (dataset["Open"] <= dataset["High"])).all()
valid_close = ((dataset["Close"] >= dataset["Low"]) & (dataset["Close"] <= dataset["High"])).all()
valid_volume = (dataset["Volume"] >= 0).all()

accuracy_checks_passed = sum([valid_high_low, valid_open, valid_close, valid_volume])
accuracy = (accuracy_checks_passed / 4) * 100

# 4. Consistency
# Here I check whether the dataset keeps a stable and correct structure.
# I verify:
# - correct column names
# - correct data types
# - no duplicates for the same Date and Ticker
correct_columns = list(dataset.columns) == [
    "Date", "Close", "High", "Low", "Open", "Volume", "Ticker", "Period"
]

correct_types = (
    pd.api.types.is_datetime64_any_dtype(dataset["Date"]) and
    pd.api.types.is_numeric_dtype(dataset["Close"]) and
    pd.api.types.is_numeric_dtype(dataset["High"]) and
    pd.api.types.is_numeric_dtype(dataset["Low"]) and
    pd.api.types.is_numeric_dtype(dataset["Open"]) and
    pd.api.types.is_numeric_dtype(dataset["Volume"]) and
    pd.api.types.is_string_dtype(dataset["Ticker"]) and
    pd.api.types.is_string_dtype(dataset["Period"])
)

no_duplicates = dataset.duplicated(subset=["Date", "Ticker"]).sum() == 0

consistency_checks_passed = sum([correct_columns, correct_types, no_duplicates])
consistency = (consistency_checks_passed / 3) * 100

# Extra prints so I can see why the consistency result is what it is
print("\nConsistency checks:")
print("Correct columns:", correct_columns)
print("Correct types:", correct_types)
print("No duplicates:", no_duplicates)

duplicate_count = dataset.duplicated(subset=["Date", "Ticker"]).sum()
print("Duplicate Date-Ticker rows:", duplicate_count)

# Final KPI results
print("\nKPI Results:")
print(f"Completeness: {completeness:.2f}%")
print(f"Latency: {latency_days} day(s)")
print(f"Accuracy: {accuracy:.2f}%")
print(f"Consistency: {consistency:.2f}%")