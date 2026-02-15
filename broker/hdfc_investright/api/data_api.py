"""
HDFC Investright Market Data API
Fetches market data, quotes, and historical data
"""

import json
import logging
from typing import Dict, List, Optional

from broker.hdfc_investright.api.baseurl import get_url
from utils.httpx_client import get_httpx_client
from utils.logging import get_logger

logger = get_logger(__name__)


def get_api_response(endpoint: str, auth: str, method: str = "GET", params: Dict = None) -> Dict:
    """Make authenticated request to HDFC market data API"""
    client = get_httpx_client()
    
    headers = {
        "Authorization": f"Bearer {auth}",
        "Content-Type": "application/json"
    }
    
    url = get_url(endpoint)
    
    try:
        if method == "GET":
            response = client.get(url, headers=headers, params=params or {})
        else:
            response = client.request(method, url, headers=headers)
        
        response.status = response.status_code
        
        return response.json() if response.text else {}
    
    except Exception as e:
        logger.error(f"API request failed: {str(e)}")
        return {"status": "error", "message": str(e)}


def get_quotes(symbol: str, exchange: str, auth: str) -> Dict:
    """
    Get live quote for a symbol
    
    Args:
        symbol: Trading symbol
        exchange: Exchange code (NSE, BSE, NFO, etc.)
        auth: Bearer token
        
    Returns:
        Quote data
    """
    try:
        params = {
            "symbol": symbol,
            "exchange": exchange
        }
        response = get_api_response("/quotes", auth, params=params)
        return response
    
    except Exception as e:
        logger.error(f"Error fetching quote for {symbol}: {str(e)}")
        return {"status": "error"}


def get_history(
    symbol: str,
    exchange: str,
    interval: str,
    start_date: str,
    end_date: str,
    auth: str
) -> Dict:
    """
    Get historical OHLC data
    
    Args:
        symbol: Trading symbol
        exchange: Exchange code
        interval: Candle interval (1m, 5m, 15m, 30m, 60m, 1d)
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        auth: Bearer token
        
    Returns:
        Historical data
    """
    try:
        params = {
            "symbol": symbol,
            "exchange": exchange,
            "interval": interval,
            "start_date": start_date,
            "end_date": end_date
        }
        response = get_api_response("/history", auth, params=params)
        return response
    
    except Exception as e:
        logger.error(f"Error fetching history for {symbol}: {str(e)}")
        return {"status": "error", "candles": []}


def get_depth(symbol: str, exchange: str, auth: str) -> Dict:
    """
    Get market depth (order book)
    
    Args:
        symbol: Trading symbol
        exchange: Exchange code
        auth: Bearer token
        
    Returns:
        Market depth data
    """
    try:
        params = {
            "symbol": symbol,
            "exchange": exchange
        }
        response = get_api_response("/depth", auth, params=params)
        return response
    
    except Exception as e:
        logger.error(f"Error fetching depth for {symbol}: {str(e)}")
        return {"status": "error"}
