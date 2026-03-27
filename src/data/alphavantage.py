"""
Alpha Vantage Data Provider for KTB Fund Manager.

Free tier: 25 API calls/day, 5 calls/minute.
Requires API key from: https://www.alphavantage.co/support/#api-key
"""

import os
import time
from typing import Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
BASE_URL = "https://www.alphavantage.co/query"
RATE_LIMIT_DELAY = 12
_last_call_time = 0


def _rate_limited_request(url: str) -> Dict[str, Any]:
    global _last_call_time
    elapsed = time.time() - _last_call_time
    if elapsed < RATE_LIMIT_DELAY:
        wait_time = RATE_LIMIT_DELAY - elapsed
        print(f"  Rate limit: waiting {wait_time:.1f}s...")
        time.sleep(wait_time)
    
    try:
        response = requests.get(url, timeout=30)
        _last_call_time = time.time()
        data = response.json()
        
        if "Note" in data and "API call frequency" in data["Note"]:
            time.sleep(15)
            return _rate_limited_request(url)
        
        return data
    except Exception as e:
        print(f"  API error: {e}")
        return {"error": str(e)}


def get_company_overview(symbol: str) -> Dict[str, Any]:
    params = f"function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
    return _rate_limited_request(f"{BASE_URL}?{params}")


def get_daily_prices(symbol: str, outputsize: str = "compact") -> Dict[str, Any]:
    params = f"function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}&apikey={API_KEY}"
    return _rate_limited_request(f"{BASE_URL}?{params}")


def get_latest_quote(symbol: str) -> Dict[str, Any]:
    params = f"function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    return _rate_limited_request(f"{BASE_URL}?{params}")


def safe_float(value, default=0.0):
    if value is None or value == "None" or value == "":
        return default
    try:
        return float(str(value).replace(",", ""))
    except:
        return default


def fetch_ticker_data(symbol: str, full: bool = False) -> Dict[str, Any]:
    print(f"\n  Fetching data for {symbol}...")
    
    data = {
        "symbol": symbol.upper(),
        "overview": {},
        "prices": {},
        "quote": {},
        "error": None
    }
    
    try:
        print("    Company overview...")
        data["overview"] = get_company_overview(symbol)
        
        print("    Latest quote...")
        quote_data = get_latest_quote(symbol)
        data["quote"] = quote_data.get("Global Quote", {})
        
        print("    Historical prices...")
        data["prices"] = get_daily_prices(symbol, "full" if full else "compact")
        
    except Exception as e:
        data["error"] = str(e)
        print(f"    Error: {e}")
    
    return data


def calculate_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
    o = data.get("overview", {})
    q = data.get("quote", {})
    
    try:
        price = safe_float(q.get("05. price"))
        if price == 0:
            prices = data.get("prices", {})
            ts = prices.get("Time Series (Daily)", {})
            if ts:
                first = list(ts.keys())[0]
                price = safe_float(ts[first].get("4. close"))
    except:
        price = 0
    
    return {
        "price": price,
        "market_cap": safe_float(o.get("MarketCapitalization")),
        "pe_ratio": safe_float(o.get("PERatio")),
        "pb_ratio": safe_float(o.get("PriceToBookRatio")),
        "peg_ratio": safe_float(o.get("PEGRatio")),
        "debt_to_equity": safe_float(o.get("DebtToEquityRatio")),
        "roe": safe_float(o.get("ReturnOnEquityTTM")) * 100,
        "roa": safe_float(o.get("ReturnOnAssetsTTM")) * 100,
        "operating_margin": safe_float(o.get("OperatingMarginTTM")) * 100,
        "profit_margin": safe_float(o.get("ProfitMargin")) * 100,
        "revenue": safe_float(o.get("RevenueTTM")),
        "eps": safe_float(o.get("EPS")),
        "dividend_yield": safe_float(o.get("DividendYield")) * 100,
        "52_week_high": safe_float(o.get("52WeekHigh")),
        "52_week_low": safe_float(o.get("52WeekLow")),
    }


def format_for_agent(data: Dict, metrics: Dict) -> str:
    o = data.get("overview", {})
    return f"""
COMPANY: {o.get('Name', 'N/A')} ({data.get('symbol', 'N/A')})
Sector: {o.get('Sector', 'N/A')} | Industry: {o.get('Industry', 'N/A')}

PRICE: ${metrics.get('price', 0):.2f}
Market Cap: ${metrics.get('market_cap', 0)/1e9:.2f}B
52-Week Range: ${metrics.get('52_week_low', 0):.2f} - ${metrics.get('52_week_high', 0):.2f}

VALUATION:
  P/E Ratio: {metrics.get('pe_ratio', 0):.2f}
  P/B Ratio: {metrics.get('pb_ratio', 0):.2f}
  PEG Ratio: {metrics.get('peg_ratio', 0):.2f}

PROFITABILITY:
  ROE: {metrics.get('roe', 0):.2f}%
  ROA: {metrics.get('roa', 0):.2f}%
  Operating Margin: {metrics.get('operating_margin', 0):.2f}%
  Profit Margin: {metrics.get('profit_margin', 0):.2f}%

BALANCE SHEET:
  Debt/Equity: {metrics.get('debt_to_equity', 0):.2f}
  Revenue: ${metrics.get('revenue', 0)/1e9:.2f}B
  EPS: ${metrics.get('eps', 0):.2f}

INCOME:
  Dividend Yield: {metrics.get('dividend_yield', 0):.2f}%
"""


if __name__ == "__main__":
    # Test with IBM (demo key works)
    data = fetch_ticker_data("IBM")
    metrics = calculate_metrics(data)
    print(format_for_agent(data, metrics))
