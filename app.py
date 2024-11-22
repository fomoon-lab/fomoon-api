from flask import Flask, jsonify
from config import (
    TOTAL_SUPPLY,
    TOKENS_PER_MINT,
    TOTAL_MINTS,
    DEV_WALLET_BALANCE,
    CIRCULATING_SUPPLY,
    TOKEN_NAME,
    TOKEN_TICKER
)

app = Flask(__name__)

@app.route('/')
def home():
    """
    Root route to provide basic information.
    """
    return (
        "Welcome to the FOMOON API! Available endpoints: "
        "/circulating_supply, /total_supply"
    )

@app.route('/circulating_supply', methods=['GET'])
def get_circulating_supply():
    """
    Endpoint to return the circulating supply.
    Circulating Supply = Total Supply - Dev Wallet Balance
    """
    try:
        response = {
            "token_name": TOKEN_NAME,
            "ticker": TOKEN_TICKER,
            "circulating_supply": CIRCULATING_SUPPLY
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch circulating supply.", "details": str(e)}), 500

@app.route('/total_supply', methods=['GET'])
def get_total_supply():
    """
    Endpoint to return the total supply and other tokenomics details.
    """
    try:
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
        return jsonify({"error": "Failed to fetch total supply details.", "details": str(e)}), 500

@app.errorhandler(404)
def page_not_found(error):
    """
    Custom error handler for 404 - Page Not Found.
    """
    return jsonify({"error": "Endpoint not found. Check available endpoints at '/'."}), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Custom error handler for 500 - Internal Server Error.
    """
    return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
