from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import numpy as np

app = Flask(__name__)
CORS(app)  # allow frontend JS requests

@app.route("/api/stock")
def get_stock_data():
    symbol = request.args.get("symbol", "").upper()
    if not symbol:
        return jsonify({"error": "Missing stock symbol"}), 400

    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="7d")

        if hist.empty:
            return jsonify({"error": "No data found"}), 404

        prices = hist["Close"].tolist()
        dates = hist.index.strftime("%a").tolist()

        # Simple indicator: compare last price with 3-day average
        avg_recent = np.mean(prices[-3:])
        signal = "BUY" if prices[-1] > avg_recent else "SELL"

        return jsonify({
            "symbol": symbol,
            "dates": dates,
            "prices": prices,
            "signal": signal
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
