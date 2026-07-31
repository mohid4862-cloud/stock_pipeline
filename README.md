# Stock Market Data Pipeline

An automated data engineering pipeline that collects, stores, and transforms 
real-time stock market data.

## What it does
- Extracts live stock price data from Yahoo Finance API
- Loads data into PostgreSQL database
- Transforms data using dbt models
- Tracks daily price changes and moving averages

## Tech Stack
- Python 3.11
- PostgreSQL
- dbt (data build tool)
- Yahoo Finance API (yfinance)
- Git

## Pipeline Architecture
## dbt Models
- `stock_summary` — average, max, min closing price per ticker
- `daily_price_change` — daily price movement using lag() window function
- `moving_average` — 3 day moving average to identify price trends

## Stocks Tracked
- AAPL (Apple)
- GOOGL (Google)
- MSFT (Microsoft)
- AMZN (Amazon)

## How to run
1. Run ETL pipeline: `python stock_pipeline.py`
2. Run dbt models: `dbt run`

## Author
Muhammad Mohid Khan
Data Analyst | Aspiring Data Engineer
GitHub: github.com/mohid4862-cloud