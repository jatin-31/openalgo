"""
HDFC Investright Order Management API
Implements order placement, modification, and cancellation
"""

import json
import logging
from typing import Dict, Optional, List

import httpx

from broker.hdfc_investright.api.baseurl import get_url
from broker.hdfc_investright.mapping import transform_data
from database.token_db import get_br_symbol, get_oa_symbol
from utils.httpx_client import get_httpx_client
from utils.logging import get_logger

logger = get_logger(__name__)


def get_api_response(endpoint: str, auth: str, method: str = "GET", payload: str = "") -> Dict:
    """
    Make authenticated HTTP request to HDFC API
    
    Args:
        endpoint: API endpoint (e.g., "/orders")
        auth: Bearer token
        method: HTTP method (GET, POST, PUT, DELETE)
        payload: JSON payload for POST/PUT requests
        
    Returns:
        Response JSON
    """
    client = get_httpx_client()
    
    headers = {
        "Authorization": f"Bearer {auth}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    url = get_url(endpoint)
    
    logger.debug(f"Request: {method} {url}")
    
    try:
        if method == "GET":
            response = client.get(url, headers=headers)
        elif method == "POST":
            response = client.post(url, headers=headers, content=payload)
        elif method == "PUT":
            response = client.put(url, headers=headers, content=payload)
        elif method == "DELETE":
            response = client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.status = response.status_code
        
        if response.status_code in [200, 201]:
            return response.json() if response.text else {"status": "success"}
        else:
            error_response = response.json() if response.text else {}
            logger.error(f"API error: {response.status_code} - {error_response}")
            return error_response
    
    except Exception as e:
        logger.error(f"API request failed: {str(e)}")
        return {"status": "error", "message": str(e)}


def place_order(order: Dict, auth: str) -> Dict:
    """
    Place a new order on HDFC Investright
    
    OpenAlgo order format:
    {
        "symbol": "INFY",
        "exchange": "NSE",
        "price": 1500.00,
        "quantity": 1,
        "side": "BUY",
        "order_type": "MARKET",
        "product": "MIS"
    }
    """
    try:
        # Transform OpenAlgo order to HDFC format
        hdfc_order = transform_data.map_order_to_hdfc(order)
        
        payload = json.dumps(hdfc_order)
        
        response = get_api_response("/orders", auth, method="POST", payload=payload)
        
        # Transform response back to OpenAlgo format
        return transform_data.map_hdfc_order_response(response)
    
    except Exception as e:
        logger.error(f"Error placing order: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def modify_order(order_id: str, order: Dict, auth: str) -> Dict:
    """
    Modify an existing order
    
    Args:
        order_id: Order ID to modify
        order: Order data with new values
        auth: Bearer token
        
    Returns:
        Modified order response
    """
    try:
        hdfc_order = transform_data.map_order_to_hdfc(order)
        payload = json.dumps(hdfc_order)
        
        response = get_api_response(f"/orders/{order_id}", auth, method="PUT", payload=payload)
        return transform_data.map_hdfc_order_response(response)
    
    except Exception as e:
        logger.error(f"Error modifying order {order_id}: {str(e)}")
        return {"status": "error", "message": str(e)}


def cancel_order(order_id: str, auth: str) -> Dict:
    """Cancel an existing order"""
    try:
        response = get_api_response(f"/orders/{order_id}", auth, method="DELETE")
        return response
    
    except Exception as e:
        logger.error(f"Error canceling order {order_id}: {str(e)}")
        return {"status": "error", "message": str(e)}


def get_order(order_id: str, auth: str) -> Dict:
    """Get details of a specific order"""
    try:
        response = get_api_response(f"/orders/{order_id}", auth, method="GET")
        return transform_data.map_hdfc_order_response(response)
    
    except Exception as e:
        logger.error(f"Error fetching order {order_id}: {str(e)}")
        return {"status": "error", "message": str(e)}


def get_order_book(auth: str) -> Dict:
    """
    Get all orders for the day
    
    Returns orders in OpenAlgo format
    """
    try:
        response = get_api_response("/orders", auth, method="GET")
        
        if response.get("status") == "error":
            return {"status": "error", "orders": []}
        
        orders = response.get("orders", [])
        transformed_orders = [transform_data.map_hdfc_order_response(order) for order in orders]
        
        return {
            "status": "success",
            "orders": transformed_orders
        }
    
    except Exception as e:
        logger.error(f"Error fetching order book: {str(e)}")
        return {"status": "error", "orders": []}


def get_trade_book(auth: str) -> Dict:
    """Get all trades executed today"""
    try:
        response = get_api_response("/trades/book", auth, method="GET")
        
        if response.get("status") == "error":
            return {"status": "error", "trades": []}
        
        trades = response.get("trades", [])
        transformed_trades = [transform_data.map_hdfc_trade_response(trade) for trade in trades]
        
        return {
            "status": "success",
            "trades": transformed_trades
        }
    
    except Exception as e:
        logger.error(f"Error fetching trade book: {str(e)}")
        return {"status": "error", "trades": []}


def get_positions(auth: str) -> Dict:
    """Get all open positions"""
    try:
        response = get_api_response("/positions", auth, method="GET")
        
        if response.get("status") == "error":
            return {"status": "error", "positions": []}
        
        positions = response.get("positions", [])
        transformed_positions = [transform_data.map_hdfc_position(pos) for pos in positions]
        
        return {
            "status": "success",
            "positions": transformed_positions
        }
    
    except Exception as e:
        logger.error(f"Error fetching positions: {str(e)}")
        return {"status": "error", "positions": []}


def get_holdings(auth: str) -> Dict:
    """Get portfolio holdings (delivery)"""
    try:
        response = get_api_response("/holdings", auth, method="GET")
        
        if response.get("status") == "error":
            return {"status": "error", "holdings": []}
        
        holdings = response.get("holdings", [])
        transformed_holdings = [transform_data.map_hdfc_holding(holding) for holding in holdings]
        
        return {
            "status": "success",
            "holdings": transformed_holdings
        }
    
    except Exception as e:
        logger.error(f"Error fetching holdings: {str(e)}")
        return {"status": "error", "holdings": []}


def get_open_position(tradingsymbol: str, exchange: str, producttype: str, auth: str) -> Dict:
    """
    Get open position for a specific symbol
    
    Args:
        tradingsymbol: OpenAlgo symbol
        exchange: Exchange code
        producttype: Product type (MIS, CNC, NRML)
        auth: Bearer token
        
    Returns:
        Position data or empty if not found
    """
    try:
        positions_response = get_positions(auth)
        positions = positions_response.get("positions", [])
        
        # Convert to broker symbol for comparison
        br_symbol = get_br_symbol(tradingsymbol, exchange)
        
        for position in positions:
            if (position.get("tradingsymbol") == br_symbol and 
                position.get("exchange") == exchange):
                return position
        
        return {}
    
    except Exception as e:
        logger.error(f"Error getting open position: {str(e)}")
        return {}
