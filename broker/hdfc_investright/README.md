# HDFC Investright Broker Integration

Complete HDFC Investright trading API integration for OpenAlgo.

## Features

✅ OAuth 2.0 Authentication with Token Refresh  
✅ Order Management (Place, Modify, Cancel)  
✅ Position & Holdings Tracking  
✅ Trade History  
✅ Market Data Quotes  
✅ Historical Data & Charts  
✅ Market Depth  
✅ Error Handling with OpenAlgo Standard Format  

## Documentation

- **API Docs**: https://developer.hdfcsec.com/ir-docs/docs/intro
- **Authentication**: https://developer.hdfcsec.com/ir-docs/docs/category/fetch-access-token-via-api
- **Orders**: https://developer.hdfcsec.com/ir-docs/docs/place_order
- **Errors**: https://developer.hdfcsec.com/ir-docs/docs/error_structure
- **Base URL**: `https://developer.hdfcsec.com/oapi/v1`

## Environment Setup

```bash
# Required environment variables
BROKER_API_KEY=your_client_id
BROKER_API_SECRET=your_client_secret
BROKER_REDIRECT_URI=http://localhost:8000/auth/callback
```

## API Endpoints Supported

### Order Management
- `POST /api/v1/orders` - Place order
- `PUT /api/v1/orders/{order_id}` - Modify order
- `DELETE /api/v1/orders/{order_id}` - Cancel order
- `GET /api/v1/orders` - Get order book
- `GET /api/v1/trades` - Get trade book

### Portfolio
- `GET /api/v1/positions` - Get positions
- `GET /api/v1/holdings` - Get holdings

### Market Data
- `GET /api/v1/quotes` - Get quotes
- `GET /api/v1/history` - Get historical data
- `GET /api/v1/depth` - Get market depth

## Usage

### Authentication Flow

```python
from broker.hdfc_investright.api import auth_api

# 1. Generate authorization URL
auth_url = auth_api.generate_auth_url()
# User visits this URL and grants permission

# 2. Exchange code for token
token_response = auth_api.get_access_token("authorization_code")
access_token = token_response["access_token"]

# 3. Use token for subsequent API calls
```

### Place Order

```python
from broker.hdfc_investright.api import order_api

order = {
    "symbol": "INFY",
    "exchange": "NSE",
    "side": "BUY",
    "quantity": 1,
    "order_type": "MARKET",
    "product": "MIS"
}

response = order_api.place_order(order, access_token)
```

### Get Positions

```python
positions = order_api.get_positions(access_token)
for pos in positions["positions"]:
    print(f"{pos['symbol']}: {pos['quantity']} @ {pos['price']}")
```

## Error Handling

All HDFC errors are mapped to OpenAlgo standard format:

```python
{
    "status": "error",
    "message": "Error description",
    "code": "HDFC_ERROR_CODE"
}
```

## Rate Limits

HDFC does not publish numeric rate limits. Implement exponential backoff on 429 responses.

## Testing

```bash
pytest broker/hdfc_investright/tests/
```
