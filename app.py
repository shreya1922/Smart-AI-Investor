from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # important for frontend connection

@app.route('/stock', methods=['GET'])
def get_stock():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({"error": "Please enter stock symbol"})

    try:
        stock = yf.Ticker(symbol + ".NS")  # NSE fix
        hist = stock.history(period='1d')

        if hist.empty:
            return jsonify({"error": "Invalid stock symbol"})

        price = hist['Close'].iloc[-1]

        # Simple AI logic
        if price > 1000:
            suggestion = "Stock is expensive. Analyze before investing."
        else:
            suggestion = "Stock looks affordable. Consider buying."

        return jsonify({
            "symbol": symbol.upper(),
            "price": round(float(price), 2),
            "suggestion": suggestion
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
