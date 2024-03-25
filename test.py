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
app = Flask(__name__)
ALLOWED_IPS = ['52.89.214.238', '34.212.75.30','54.218.53.128','52.32.178.7','127.0.0.1']
@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)  # Forbidden

@app.route('/balance', methods=['POST'])
def balance():
    data = request.get_json()
    if not data:
        logging.error("Missing data in request")
        return jsonify({'error': 'Missing data'}), 400
    # Log the entire incoming request data
    logging.info(f"Incoming webhook data: {data}")

    for order in data:
        balance = order.get('balance')
        if 'all' in balance:
            #get Account
            try:
                accountinfo = client.get_account()
                logging.info(f"getAccount: {accountinfo}")
            except BinanceAPIException as e:
                logging.info(f"BinanceAPIException occurred: {str(e)}")
            except Exception as e:
                # Catch any other exceptions that were not anticipated
                logging.exception("Unexpected exception occurred")
                return jsonify({'error': 'An unexpected error occurred'}), 500
    return jsonify({'message': 'message processed'}), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
