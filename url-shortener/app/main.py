from flask import Flask, request, jsonify, redirect, abort
from app.utils import generate_short_code, is_valid_url
from app.models import URLStore

app = Flask(__name__)
store = URLStore()

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

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    url = data.get("url")
    if not url or not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    # Ensure unique short code
    for _ in range(10):
        short_code = generate_short_code()
        if not store.get(short_code):
            store.add(short_code, url)
            short_url = f"{request.host_url}{short_code}"
            return jsonify({"short_code": short_code, "short_url": short_url}), 201
    return jsonify({"error": "Could not generate unique short code"}), 500

@app.route("/<short_code>", methods=["GET"])
def redirect_short_url(short_code):
    entry = store.get(short_code)
    if not entry:
        abort(404)
    store.increment_clicks(short_code)
    return redirect(entry["url"])

@app.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code):
    entry = store.get(short_code)
    if not entry:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify({
        "url": entry["url"],
        "clicks": entry["clicks"],
        "created_at": entry["created_at"]
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)