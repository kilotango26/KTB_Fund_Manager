"""
Unified Stock Data Provider - Alpha Vantage + yFinance fallback
"""

import os
import time
from typing import Dict, Any, Optional

# Try yFinance (always available)
try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False

# Try Alpha Vantage
try:
    from .alphavantage import fetch_ticker_data, calculate_metrics
    AV_AVAILABLE = True
except ImportError:
    AV_AVAILABLE = False


def fetch_from_yfinance(symbol: str) -> Optional[Dict[str, Any]]:
    """Fetch real-time data from Yahoo Finance. Free, no API key."""
    if not YF_AVAILABLE:
        print(f"  ⚠️ yfinance not installed")
        return None
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="2d")
        
        if len(hist) < 1 or hist['Close'].iloc[-1] == 0:
            return None
        
        current = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
        
        return {
            "source": "yfinance",
            "symbol": symbol.upper(),
            "price": current,
            "previous_close": prev,
            "change_percent": ((current - prev) / prev * 100) if prev else 0,
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", 0) or info.get("forwardPE", 0),
            "pb_ratio": info.get("priceToBook", 0),
            "eps": info.get("trailingEps", 0),
            "dividend_yield": (info.get("dividendYield") or 0) * 100,
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh", 0),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
            "revenue": info.get("totalRevenue", 0),
            "debt_to_equity": info.get("debtToEquity", 0),
            "roe": (info.get("returnOnEquity") or 0) * 100,
            "profit_margin": (info.get("profitMargins") or 0) * 100,
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "company_name": info.get("longName", symbol)
        }
    except Exception as e:
        print(f"  yFinance error: {e[:50]}")
        return None


def fetch_stock_data(symbol: str, prefer="yfinance") -> Dict[str, Any]:
    """Fetch stock data with fallback."""
    symbol = symbol.upper()
    
    # Priority: yFinance > Alpha Vantage > Error
    if prefer in ["yfinance", "auto"] and YF_AVAILABLE:
        data = fetch_from_yfinance(symbol)
        if data and data.get("price", 0) > 0:
            return data
    
    if AV_AVAILABLE:
        try:
            av_data = fetch_ticker_data(symbol)
            m = calculate_metrics(av_data)
            q = av_data.get("quote", {})
            o = av_data.get("overview", {})
            
            price = m.get("price", 0)
            if price > 0:
                return {
                    "source": "alphavantage",
                    "symbol": symbol,
                    "price": price,
                    "previous_close": float(q.get("08. previous close", price)),
                    "change_percent": float(q.get("10. change percent", "0").replace("%", "")),
                    "market_cap": m.get("market_cap", 0),
                    "pe_ratio": m.get("pe_ratio", 0),
                    "pb_ratio": m.get("pb_ratio", 0),
                    "eps": m.get("eps", 0),
                    "dividend_yield": m.get("dividend_yield", 0),
                    "fifty_two_week_high": m.get("52_week_high", 0),
                    "fifty_two_week_low": m.get("52_week_low", 0),
                    "revenue": m.get("revenue", 0),
                    "debt_to_equity": m.get("debt_to_equity", 0),
                    "roe": m.get("roe", 0),
                    "profit_margin": m.get("profit_margin", 0),
                    "sector": o.get("Sector", "Unknown"),
                    "industry": o.get("Industry", "Unknown"),
                    "company_name": o.get("Name", symbol)
                }
        except Exception as e:
            print(f"  Alpha Vantage fallback failed: {e[:50]}")
    
    # Error fallback
    return {
        "source": "error",
        "symbol": symbol,
        "price": 0.0,
        "error": "All data sources failed"
    }


if __name__ == "__main__":
    # Test
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    result = fetch_stock_data(ticker)
    print(f"\n{ticker}:")
    print(f"  Source: {result['source']}")
    print(f"  Price: ${result['price']:.2f}")
    print(f"  Change: {result['change_percent']:+.2f}%")
