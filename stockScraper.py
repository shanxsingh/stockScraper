import json
import yfinance as yf
from datetime import datetime

# List of stock symbols to fetch data for
STOCKS = ['NVDA', 'LULU', 'AAPL', 'TSLA', 'AMZN', 'GOOGL', 'MSFT', 'META', 'NFLX']

def fetch_current_stock_data(symbol):
    """Fetch today's stock price and change for a given symbol."""
    ticker = yf.Ticker(symbol)
    today_data = ticker.history(period='1d')

    if not today_data.empty:
        close_price = today_data['Close'].iloc[0]
        open_price = today_data['Open'].iloc[0]
        price_change = close_price - open_price
        return {
            'symbol': symbol,
            'price': f"{close_price:.2f}",
            'change': f"{price_change:.2f}"
        }

    return {
        'symbol': symbol,
        'price': 'N/A',
        'change': 'N/A'
    }

def fetch_monthly_stock_data(symbol):
    """Fetch the last month's historical data for a given symbol."""
    ticker = yf.Ticker(symbol)
    historical_data = ticker.history(period='1mo')
    monthly_info = []

    for date, row in historical_data.iterrows():
        monthly_info.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': round(row['Close'], 2),
            'change': round(row['Close'] - row['Open'], 2)
        })

    return monthly_info

def save_to_json(filename, data):
    """Save the provided data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    """Main function to fetch stock data and save to files."""
    stock_data = []
    monthly_data = {symbol: fetch_monthly_stock_data(symbol) for symbol in STOCKS}

    for stock in STOCKS:
        current_data = fetch_current_stock_data(stock)
        stock_data.append(current_data)
        print(f"Received data for: {current_data['symbol']}, Price: {current_data['price']}, Change: {current_data['change']}")

    # Save data to JSON files
    save_to_json('stock_data_today.json', stock_data)
    save_to_json('stock_data_month.json', monthly_data)

    print("Data fetching complete.")

if __name__ == "__main__":
    main()
