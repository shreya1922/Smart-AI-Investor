from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stock', methods=['GET'])
def get_stock():
    symbol = request.args.get('symbol')

    try:
        data = yf.Ticker(symbol)
        hist = data.history(period='1d')

        if hist.empty:
            return jsonify({"error": "Invalid stock symbol"})

        price = hist['Close'][0]

        # Simple AI suggestion
        if price > 1000:
            suggestion = "Stock price is high. Invest carefully."
        else:
            suggestion = "Stock price is moderate. You can consider buying."

        return jsonify({
            "symbol": symbol,
            "price": float(price),
            "suggestion": suggestion
        })

    except:
        return jsonify({"error": "Error fetching data"})

if __name__ == '__main__':
    app.run(debug=True)