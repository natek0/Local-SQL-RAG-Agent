import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_financial_db(path="data/finance.db"):
    conn = sqlite3.connect(path)
    
    # 1. Tickers Table
    tickers = pd.DataFrame({
        'symbol': ['AAPL', 'MSFT', 'GOOGL', 'XOM', 'CVX', 'JPM', 'GS'],
        'sector': ['Tech', 'Tech', 'Tech', 'Energy', 'Energy', 'Finance', 'Finance'],
        'name': ['Apple', 'Microsoft', 'Google', 'Exxon', 'Chevron', 'JP Morgan', 'Goldman Sachs']
    })
    tickers.to_sql('tickers', conn, if_exists='replace', index=False)
    
    # 2. Stock Prices (Random Walk Generation)
    dates = pd.date_range(end=datetime.today(), periods=100)
    data = []
    
    for _, row in tickers.iterrows():
        price = 100
        for date in dates:
            change = np.random.normal(0, 2) # Random walk
            price += change
            data.append({
                'symbol': row['symbol'],
                'date': date.strftime('%Y-%m-%d'),
                'close_price': round(price, 2),
                'volume': np.random.randint(1000, 1000000)
            })
            
    prices = pd.DataFrame(data)
    prices.to_sql('stock_prices', conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"Financial Database created at {path}")

if __name__ == "__main__":
    create_financial_db()
