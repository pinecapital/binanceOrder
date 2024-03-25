from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException


import os
import logging  # Import the logging module
logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s',filemode='w')

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

# Initialize Binance client for Spot trading
client = Client(api_key, secret_key)

#get Account
try:
    accountinfo = client.get_account()
    logging.info(f"getAccount: {accountinfo}")
except BinanceAPIException as e:
    logging.info(f"BinanceAPIException occurred: {str(e)}")