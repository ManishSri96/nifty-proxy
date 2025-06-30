from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/nifty')
def get_nifty_data():
    try:
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com/option-chain",
        }
        session.headers.update(headers)

        # Get homepage to set cookies (increase timeout to 10)
        session.get("https://www.nseindia.com", timeout=10)

        # Get option chain data (timeout also 10)
        response = session.get("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY", timeout=10)

        if response.status_code != 200:
            return jsonify({"error": f"NSE API returned {response.status_code}"})

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
