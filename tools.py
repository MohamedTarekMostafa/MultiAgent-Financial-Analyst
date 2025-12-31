import yfinance as yf
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv
load_dotenv(".env")
search = TavilySearch(max_results=5)

@tool
def get_market_data(ticker: str) -> str:
    """Fetch current stock price and change for a ticker (e.g., 'NVIDIA')."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        change = info.get('regularMarketChangePercent', 0)
        return f"Price: ${price}, Change: {change:.2f}%."
    except Exception as e:
        return f"Error: {e}"

@tool
def web_search(query: str):
    """Search the web for news and real-time info."""
    return search.run(query)

financial_tools = [get_market_data, web_search]