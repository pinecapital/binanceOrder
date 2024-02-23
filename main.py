from flask import Flask, request, jsonify
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

import os
import logging  # Import the logging module

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

# Initialize Binance client for Spot trading
client = Client(api_key, secret_key)

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s',filemode='w')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        logging.error("Missing data in request")
        return jsonify({'error': 'Missing data'}), 400
    # Log the entire incoming request data
    logging.info(f"Incoming webhook data: {data}")

    for order in data:
        symbol = order.get('symbol')
        if 'side' in order:
            side = order['side'].upper()
            size = float(order['size'])
            try:
                if side == 'BUY':
                    response = client.order_market_buy(symbol=symbol, quantity=size)
                elif side == 'SELL':
                    response = client.order_market_sell(symbol=symbol, quantity=size)
                else:
                    logging.error("Invalid order side")
                    return jsonify({'error': 'Invalid side'}), 400
            except BinanceAPIException as e:
                # Handle specific Binance API exceptions
                logging.error(f"BinanceAPIException occurred: {str(e)}")
                return jsonify({'error': f"Binance API error: {str(e)}"}), 500
            except Exception as e:
                # Catch any other exceptions that were not anticipated
                logging.exception("Unexpected exception occurred")
                return jsonify({'error': 'An unexpected error occurred'}), 500
        elif 'closepos' in order and order['closepos']:
            logging.warning("Attempt to close position in Spot market")
            return jsonify({'error': 'Closing positions not directly supported in Spot market'}), 400
        else:
            logging.error("Invalid order format")
            return jsonify({'error': 'Invalid order format'}), 400

    logging.info("All orders processed successfully")
    return jsonify({'message': 'Orders processed'}), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
