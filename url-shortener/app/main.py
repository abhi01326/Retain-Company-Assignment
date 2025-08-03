from flask import Flask, request, jsonify, redirect
from app.models import save_url, get_url, increment_click, get_stats
from app.utils import is_valid_url, generate_short_code
app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })
@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    url = data.get("url")

    if not url or not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while get_url(short_code):
        short_code = generate_short_code()

    save_url(short_code, url)
    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    })

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    url = get_url(short_code)
    if not url:
        return jsonify({"error": "Short code not found"}), 404
    increment_click(short_code)
    return redirect(url)

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    stat = get_stats(short_code)
    if not stat:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify(stat)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
