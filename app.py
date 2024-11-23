from flask import Flask, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from config import (
    TOTAL_SUPPLY,
    TOKENS_PER_MINT,
    TOTAL_MINTS,
    DEV_WALLET_BALANCE,
    CIRCULATING_SUPPLY,
    TOKEN_NAME,
    TOKEN_TICKER
)

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

@app.route('/')
def home():
    """
    Root route to render the UI.
    """
    logging.info("Home endpoint accessed")
    return render_template("index.html")

@app.route('/circulating_supply', methods=['GET'])
@limiter.limit("10 per minute")
def get_circulating_supply():
    """
    Endpoint to return the circulating supply.
    Circulating Supply = Total Supply - Dev Wallet Balance
    """
    try:
        logging.info("Circulating supply endpoint accessed")
        response = {
            "token_name": TOKEN_NAME,
            "ticker": TOKEN_TICKER,
            "circulating_supply": CIRCULATING_SUPPLY
        }
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Error fetching circulating supply: {e}")
        return jsonify({"error": "Failed to fetch circulating supply.", "details": str(e)}), 500

@app.route('/total_supply', methods=['GET'])
@limiter.limit("10 per minute")
def get_total_supply():
    """
    Endpoint to return the total supply and other tokenomics details.
    """
    try:
        logging.info("Total supply endpoint accessed")
        response = {
            "token_name": TOKEN_NAME,
            "ticker": TOKEN_TICKER,
            "total_supply": TOTAL_SUPPLY,
            "tokens_per_mint": TOKENS_PER_MINT,
            "total_mints": TOTAL_MINTS,
            "dev_wallet_balance": DEV_WALLET_BALANCE
        }
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Error fetching total supply details: {e}")
        return jsonify({"error": "Failed to fetch total supply details.", "details": str(e)}), 500

@app.errorhandler(404)
def page_not_found(error):
    """
    Custom error handler for 404 - Page Not Found.
    """
    logging.warning("404 error - endpoint not found")
    return jsonify({"error": "Endpoint not found. Check available endpoints at '/'."}), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Custom error handler for 500 - Internal Server Error.
    """
    logging.error(f"500 error - {error}")
    return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
