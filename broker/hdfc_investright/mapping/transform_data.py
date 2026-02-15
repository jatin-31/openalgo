"""
HDFC Investright Data Transformation
Maps between OpenAlgo and HDFC Investright formats
"""

import logging
from typing import Dict, Optional

from database.token_db import get_br_symbol, get_oa_symbol
from utils.logging import get_logger

logger = get_logger(__name__)


# Order type mapping
ORDER_TYPE_MAP = {
    "MARKET": "MKT",
    "LIMIT": "LMT",
    "STOP_LOSS": "SL",
    "STOP_LOSS_LIMIT": "SLL"
}

ORDER_TYPE_REVERSE_MAP = {v: k for k, v in ORDER_TYPE_MAP.items()}

# Product type mapping
PRODUCT_MAP = {
    "MIS": "MIS",
    "INTRADAY": "MIS",
    "CNC": "CNC",
    "DELIVERY": "CNC",
    "NRML": "NRML",
    "MARGIN": "NRML"
}

PRODUCT_REVERSE_MAP = {
    "MIS": "MIS",
    "CNC": "CNC",
    "NRML": "NRML"
}

# Side mapping
SIDE_MAP = {
    "BUY": "BUY",
    "SELL": "SELL"
}

# Validity mapping
VALIDITY_MAP = {
    "DAY": "DAY",
    "IOC": "IOC",
    "GTC": "GTC"
}


def map_order_to_hdfc(order: Dict) -> Dict:
    """
    Convert OpenAlgo order format to HDFC Investright format
    
    Args:
        order: OpenAlgo order dict with keys: symbol, exchange, side, quantity, 
               price, order_type, product, validity
               
    Returns:
        HDFC order format
    """
    try:
        symbol = order.get("symbol", "")
        exchange = order.get("exchange", "")
        
        # Convert symbol to broker format
        br_symbol = get_br_symbol(symbol, exchange)
        if not br_symbol:
            br_symbol = symbol
        
        hdfc_order = {
            "symbol": br_symbol,
            "exchange": exchange,
            "side": SIDE_MAP.get(order.get("side", "BUY"), "BUY"),
            "quantity": int(order.get("quantity", 0)),
            "order_type": ORDER_TYPE_MAP.get(order.get("order_type", "MARKET"), "MKT"),
            "product": PRODUCT_MAP.get(order.get("product", "MIS"), "MIS"),
            "validity": VALIDITY_MAP.get(order.get("validity", "DAY"), "DAY")
        }
        
        # Add optional fields
        if order.get("price"):
            hdfc_order["price"] = float(order["price"])
        
        if order.get("stop_price"):
            hdfc_order["stop_price"] = float(order["stop_price"])
        
        if order.get("disclosed_quantity"):
            hdfc_order["disclosed_quantity"] = int(order["disclosed_quantity"])
        
        logger.debug(f"Mapped order to HDFC format: {hdfc_order}")
        return hdfc_order
    
    except Exception as e:
        logger.error(f"Error mapping order: {str(e)}")
        raise


def map_hdfc_order_response(hdfc_order: Dict) -> Dict:
    """
    Convert HDFC order response to OpenAlgo format
    
    Args:
        hdfc_order: HDFC order response
        
    Returns:
        OpenAlgo order format
    """
    try:
        # Get OpenAlgo symbol from broker symbol
        exchange = hdfc_order.get("exchange", "")
        br_symbol = hdfc_order.get("symbol", "")
        oa_symbol = get_oa_symbol(br_symbol, exchange)
        if not oa_symbol:
            oa_symbol = br_symbol
        
        return {
            "order_id": hdfc_order.get("order_id", ""),
            "symbol": oa_symbol,
            "exchange": exchange,
            "side": hdfc_order.get("side", ""),
            "quantity": hdfc_order.get("quantity", 0),
            "price": hdfc_order.get("price", 0),
            "order_type": ORDER_TYPE_REVERSE_MAP.get(hdfc_order.get("order_type", "MKT"), "MARKET"),
            "product": PRODUCT_REVERSE_MAP.get(hdfc_order.get("product", "MIS"), "MIS"),
            "order_status": hdfc_order.get("status", ""),
            "filled_quantity": hdfc_order.get("filled_quantity", 0),
            "pending_quantity": hdfc_order.get("pending_quantity", 0),
            "average_price": hdfc_order.get("average_price", 0),
            "timestamp": hdfc_order.get("created_at", "")
        }
    
    except Exception as e:
        logger.error(f"Error mapping HDFC order response: {str(e)}")
        return hdfc_order


def map_hdfc_trade_response(hdfc_trade: Dict) -> Dict:
    """Convert HDFC trade response to OpenAlgo format"""
    try:
        exchange = hdfc_trade.get("exchange", "")
        br_symbol = hdfc_trade.get("symbol", "")
        oa_symbol = get_oa_symbol(br_symbol, exchange)
        if not oa_symbol:
            oa_symbol = br_symbol
        
        return {
            "trade_id": hdfc_trade.get("trade_id", ""),
            "order_id": hdfc_trade.get("order_id", ""),
            "symbol": oa_symbol,
            "exchange": exchange,
            "side": hdfc_trade.get("side", ""),
            "quantity": hdfc_trade.get("quantity", 0),
            "price": hdfc_trade.get("price", 0),
            "timestamp": hdfc_trade.get("executed_at", "")
        }
    
    except Exception as e:
        logger.error(f"Error mapping trade response: {str(e)}")
        return hdfc_trade


def map_hdfc_position(hdfc_pos: Dict) -> Dict:
    """Convert HDFC position to OpenAlgo format"""
    try:
        exchange = hdfc_pos.get("exchange", "")
        br_symbol = hdfc_pos.get("symbol", "")
        oa_symbol = get_oa_symbol(br_symbol, exchange)
        if not oa_symbol:
            oa_symbol = br_symbol
        
        return {
            "symbol": oa_symbol,
            "exchange": exchange,
            "quantity": hdfc_pos.get("quantity", 0),
            "product": PRODUCT_REVERSE_MAP.get(hdfc_pos.get("product", "MIS"), "MIS"),
            "price": hdfc_pos.get("average_price", 0),
            "pnl": hdfc_pos.get("pnl", 0),
            "pnl_percentage": hdfc_pos.get("pnl_percentage", 0)
        }
    
    except Exception as e:
        logger.error(f"Error mapping position: {str(e)}")
        return hdfc_pos


def map_hdfc_holding(hdfc_holding: Dict) -> Dict:
    """Convert HDFC holding to OpenAlgo format"""
    try:
        exchange = hdfc_holding.get("exchange", "")
        br_symbol = hdfc_holding.get("symbol", "")
        oa_symbol = get_oa_symbol(br_symbol, exchange)
        if not oa_symbol:
            oa_symbol = br_symbol
        
        return {
            "symbol": oa_symbol,
            "exchange": exchange,
            "quantity": hdfc_holding.get("quantity", 0),
            "price": hdfc_holding.get("average_price", 0),
            "value": hdfc_holding.get("value", 0),
            "pnl": hdfc_holding.get("pnl", 0)
        }
    
    except Exception as e:
        logger.error(f"Error mapping holding: {str(e)}")
        return hdfc_holding
