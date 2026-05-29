import yfinance as yf


def get_price_data(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")
    info = stock.info

    if hist.empty:
        return {"error": "No price data available"}

    current_price = hist["Close"].iloc[-1]
    start_price = hist["Close"].iloc[0]
    pct_change = (current_price - start_price) / start_price * 100

    return {
        "current_price": round(float(current_price), 2),
        "price_3mo_ago": round(float(start_price), 2),
        "pct_change_3mo": round(float(pct_change), 2),
        "week52_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "week52_low": info.get("fiftyTwoWeekLow", "N/A"),
        "avg_volume": int(hist["Volume"].mean()),
        "currency": info.get("currency", "USD"),
    }


def get_financial_data(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "company_name": info.get("longName", ticker),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "eps": info.get("trailingEps", "N/A"),
        "revenue": info.get("totalRevenue"),
        "profit_margin": info.get("profitMargins"),
        "dividend_yield": info.get("dividendYield", "N/A"),
        "description": (info.get("longBusinessSummary", "") or "")[:500],
    }


def get_risk_data(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")
    info = stock.info

    if hist.empty:
        return {"error": "No data available"}

    daily_returns = hist["Close"].pct_change().dropna()
    annualized_vol = daily_returns.std() * (252 ** 0.5) * 100
    max_drawdown = (hist["Close"].min() - hist["Close"].max()) / hist["Close"].max() * 100

    return {
        "annualized_volatility": round(float(annualized_vol), 2),
        "beta": info.get("beta", "N/A"),
        "week52_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "week52_low": info.get("fiftyTwoWeekLow", "N/A"),
        "max_drawdown_6mo": round(float(max_drawdown), 2),
    }
