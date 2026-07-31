select
    ticker,
    round(avg(close_price)::numeric, 2) as avg_close,
    round(max(close_price)::numeric, 2) as max_close,
    round(min(close_price)::numeric, 2) as min_close,
    count(*) as total_days
from {{ source('public', 'stock_prices') }}
group by ticker