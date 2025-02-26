import os
import time

from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON
from py_clob_client.clob_types import OrderArgs, OrderType, TradeParams
from py_clob_client.order_builder.constants import BUY


def PlaceOrder(asset_id, poly_price, size):
    
    # Clob API key
    key = os.getenv('CLOB_API_KEY')
    
    host = "https://clob.polymarket.com"
    chain_id = POLYGON
    
    # Public address of your Polymarket account
    PUBLIC_ADRESS = "PUBLIC_ADRESS"
    
    if not key:
        raise ValueError("Private key not found. Please set PK in the environment variables.")
    client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=PUBLIC_ADRESS)
    client.set_api_creds(client.create_or_derive_api_creds())
    order_args = OrderArgs(
        price = poly_price,
        size = size,
        side = BUY,
        token_id = asset_id,
    )
    signed_order = client.create_order(order_args)
    resp = client.post_order(signed_order, OrderType.GTC)
    return (resp['success'], resp['errorMsg'])

def GetTradesLoop(market_id):
    resp_start = GetTrades(market_id)
    for i in range(5):
        resp = GetTrades(market_id)
        if resp_start != resp:
            return True
        time.sleep(1)
    return False

def GetTrades(market_id):
    
    # Clob API key
    key = os.getenv('CLOB_API_KEY')
    
    host = "https://clob.polymarket.com"
    chain_id = POLYGON
    
    # Public address of your Polymarket account
    PUBLIC_ADRESS = "PUBLIC_ADRESS"
    
    if not key:
        raise ValueError("Private key not found. Please set PK in the environment variables.")
    client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=PUBLIC_ADRESS)
    client.set_api_creds(client.create_or_derive_api_creds())
    resp = client.get_trades(
        TradeParams(
            maker_address=PUBLIC_ADRESS,
            market=market_id,
        ),
    )
    return resp

def CancelAllOrders():
    
    # Clob API key
    key = os.getenv('CLOB_API_KEY')
    
    host = "https://clob.polymarket.com"
    chain_id = POLYGON
    
    # Public address of your Polymarket account
    PUBLIC_ADRESS = "PUBLIC_ADRESS"
    
    if not key:
        raise ValueError("Private key not found. Please set PK in the environment variables.")
    client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=PUBLIC_ADRESS)
    client.set_api_creds(client.create_or_derive_api_creds())
    client.cancel_all()