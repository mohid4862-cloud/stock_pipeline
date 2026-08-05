select
    ticker,
    trade_date,
    close_price,
    round((close_price - lag(close_price) over (
        partition by ticker
        order by trade_date
    ))::numeric, 2) as price_change,
    round((((close_price - lag(close_price) over (
        partition by ticker
        order by trade_date
    )) / lag(close_price) over (
        partition by ticker
        order by trade_date
    )) * 100)::numeric, 2) as pct_change
from {{ source('public', 'stock_prices') }}
order by ticker, trade_date


