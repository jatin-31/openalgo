"""HDFC Investright broker base URLs configuration."""

# Base URLs for HDFC Investright API endpoints
BASE_URL = "https://developer.hdfcsec.com/oapi/v1"
AUTH_BASE_URL = "https://developer.hdfcsec.com"

# Derived URLs for specific API endpoints
ORDERS_URL = f"{BASE_URL}/orders"
POSITIONS_URL = f"{BASE_URL}/positions"
HOLDINGS_URL = f"{BASE_URL}/holdings"
TRADES_URL = f"{BASE_URL}/trades"
ACCOUNT_URL = f"{BASE_URL}/account"


def get_url(endpoint):
    """Get full URL for an API endpoint"""
    return f"{BASE_URL}{endpoint}"
