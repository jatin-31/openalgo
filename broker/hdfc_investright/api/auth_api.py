"""
HDFC Investright Authentication Handler
Implements OAuth 2.0 token management for OpenAlgo
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Dict

import httpx
from requests.auth import HTTPBasicAuth

from utils.httpx_client import get_httpx_client
from utils.logging import get_logger

logger = get_logger(__name__)

AUTH_BASE_URL = "https://developer.hdfcsec.com"


def generate_auth_url(state: str = "openalgo_state") -> str:
    """
    Generate OAuth 2.0 authorization URL
    
    User should open this URL in browser to grant permission
    """
    api_key = os.getenv("BROKER_API_KEY", "")
    
    if not api_key:
        raise ValueError("BROKER_API_KEY environment variable not set")
    
    redirect_uri = os.getenv("BROKER_REDIRECT_URI", "http://localhost:8000/auth/callback")
    
    auth_url = (
        f"{AUTH_BASE_URL}/oauth/authorize"
        f"?client_id={api_key}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&state={state}"
        f"&scope=trading placement"
    )
    
    return auth_url


def get_access_token(authorization_code: str) -> Optional[Dict]:
    """
    Exchange authorization code for access token
    
    Args:
        authorization_code: Code from OAuth callback
        
    Returns:
        Token response with access_token, refresh_token, expires_in
    """
    try:
        api_key = os.getenv("BROKER_API_KEY", "")
        api_secret = os.getenv("BROKER_API_SECRET", "")
        redirect_uri = os.getenv("BROKER_REDIRECT_URI", "http://localhost:8000/auth/callback")
        
        if not api_key or not api_secret:
            logger.error("BROKER_API_KEY or BROKER_API_SECRET not set")
            return None
        
        client = get_httpx_client()
        
        token_url = f"{AUTH_BASE_URL}/oauth/token"
        
        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri,
            "client_id": api_key,
            "client_secret": api_secret
        }
        
        response = client.post(
            token_url,
            data=payload,
            auth=HTTPBasicAuth(api_key, api_secret)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get access token: {response.text}")
            return None
    
    except Exception as e:
        logger.error(f"Exception in get_access_token: {str(e)}")
        return None


def refresh_access_token(refresh_token: str) -> Optional[Dict]:
    """
    Refresh expired access token
    
    Args:
        refresh_token: Previously issued refresh token
        
    Returns:
        New token response
    """
    try:
        api_key = os.getenv("BROKER_API_KEY", "")
        api_secret = os.getenv("BROKER_API_SECRET", "")
        
        if not api_key or not api_secret:
            logger.error("BROKER_API_KEY or BROKER_API_SECRET not set")
            return None
        
        client = get_httpx_client()
        
        token_url = f"{AUTH_BASE_URL}/oauth/token"
        
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": api_key,
            "client_secret": api_secret
        }
        
        response = client.post(
            token_url,
            data=payload,
            auth=HTTPBasicAuth(api_key, api_secret)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to refresh token: {response.text}")
            return None
    
    except Exception as e:
        logger.error(f"Exception in refresh_access_token: {str(e)}")
        return None


def validate_token(access_token: str) -> bool:
    """
    Validate if access token is still valid
    
    Args:
        access_token: Token to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        client = get_httpx_client()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Try to fetch account info as validation
        response = client.get(
            f"{AUTH_BASE_URL}/oapi/v1/account/profile",
            headers=headers,
            timeout=5.0
        )
        
        return response.status_code == 200
    
    except Exception as e:
        logger.warning(f"Token validation failed: {str(e)}")
        return False
