from flask import Flask, jsonify

app = Flask(__name__)

# Constants
TOTAL_SUPPLY = 1_000_000_000
TOKENS_PER_MINT = 2_000
TOTAL_MINTS = 500_000
DEV_WALLET_BALANCE = 8_898_199
CIRCULATING_SUPPLY = TOTAL_SUPPLY - DEV_WALLET_BALANCE
TOKEN_NAME = "FOMOON"
TOKEN_TICKER = "FOMOON"

@app.route('/')
def home():
    """
    Root route to provide basic information.
    """
    return "Welcome to the FOMOON API! Available endpoints: /circulating_supply, /total_supply"

@app.route('/circulating_supply', methods=['GET'])
def get_circulating_supply():
    """
    Endpoint to return the circulating supply.
    Circulating Supply = Total Supply - Dev Wallet Balance
    """
    response = {
        "token_name": TOKEN_NAME,
        "ticker": TOKEN_TICKER,
        "circulating_supply": CIRCULATING_SUPPLY
    }
    return jsonify(response), 200

@app.route('/total_supply', methods=['GET'])
def get_total_supply():
    """
    Endpoint to return the total supply and other tokenomics details.
    """
    response = {
        "token_name": TOKEN_NAME,
        "ticker": TOKEN_TICKER,
        "total_supply": TOTAL_SUPPLY,
        "tokens_per_mint": TOKENS_PER_MINT,
        "total_mints": TOTAL_MINTS,
        "dev_wallet_balance": DEV_WALLET_BALANCE
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
