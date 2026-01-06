PRICES = {
    "NVDA": 150.0,
    "AAPL": 200.0,
    "MSFT": 300.0,
}

def get_stock_price(ticker: str) -> float:
    """Gets the current stock price for a given ticker."""
    ticker = ticker.upper()
    print(f'--- TOOL CALLED: get_stock_price(ticker="{ticker}") ---')
    return PRICES.get(ticker, 0.0)
