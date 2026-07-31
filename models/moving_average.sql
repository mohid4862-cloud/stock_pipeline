select
    ticker,
    trade_date,
    close_price,
    round(avg(close_price) over (
        partition by ticker
        order by trade_date
        rows between 2 preceding and current row
    )::numeric, 2) as moving_avg_3day
from {{ source('public', 'stock_prices') }}
order by ticker, trade_date
