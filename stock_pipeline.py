import yfinance as yf
import psycopg2
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Config
DB_CONFIG = {
    "host": "localhost",
    "database": "stock_pipeline",
    "user": "postgres",
    "password": "tiger"
}
TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN"]

def connect_db():
    """Connect to PostgreSQL database."""
    conn = psycopg2.connect(**DB_CONFIG)
    logger.info("Database connected successfully")
    return conn

def create_table(conn):
    """Create stock_prices table if not exists."""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id SERIAL PRIMARY KEY,
            ticker TEXT,
            open_price REAL,
            close_price REAL,
            high_price REAL,
            low_price REAL,
            volume BIGINT,
            trade_date DATE,
            loaded_at TEXT
        )
    """)
    conn.commit()
    logger.info("Table created successfully")
    return cur

def extract(ticker, period="5d"):
    """
    Extract stock price history from Yahoo Finance.
    
    Args:
        ticker: Stock symbol e.g. 'AAPL'
        period: Time period e.g. '5d', '1mo', '3mo'
    
    Returns:
        DataFrame with stock price history
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df

def load(cur, conn, ticker, df, loaded_at):
    """Load stock data into PostgreSQL."""
    for date, row in df.iterrows():
        cur.execute("""
            INSERT INTO stock_prices 
            (ticker, open_price, close_price, high_price, low_price, volume, trade_date, loaded_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            ticker,
            round(float(row['Open']), 2),
            round(float(row['Close']), 2),
            round(float(row['High']), 2),
            round(float(row['Low']), 2),
            int(row['Volume']),
            date.date(),
            loaded_at
        ))
    conn.commit()
    logger.info(f"{ticker}: loaded successfully")

def run_pipeline():
    """Run the full ETL pipeline."""
    conn = connect_db()
    cur = create_table(conn)
    loaded_at = datetime.now().isoformat(timespec="seconds")

    for ticker in TICKERS:
        try:
            df = extract(ticker)
            if df.empty:
                logger.warning(f"{ticker}: No data returned — skipping")
                continue
            load(cur, conn, ticker, df, loaded_at)
        except Exception as e:
            logger.error(f"{ticker}: failed — {e}")
            continue

    cur.close()
    conn.close()
    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()