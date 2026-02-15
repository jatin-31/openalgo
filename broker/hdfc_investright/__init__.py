"""
HDFC Investright Broker Integration for OpenAlgo
Complete OAuth 2.0 authentication and trading API client

Documentation: https://developer.hdfcsec.com/ir-docs/docs/intro
Base URL: https://developer.hdfcsec.com/oapi/v1/

Features:
- OAuth 2.0 authentication with token refresh
- Order placement, modification, and cancellation
- Position and trade tracking
- Standardized error handling with OpenAlgo format
- Rate limit awareness
"""

from broker.hdfc_investright.api import auth_api, order_api, data_api
from broker.hdfc_investright.mapping import transform_data

__version__ = "1.0.0"
__all__ = ["auth_api", "order_api", "data_api", "transform_data"]
