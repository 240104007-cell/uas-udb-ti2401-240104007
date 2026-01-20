"""
Clickjacking Vulnerability Checker
A simple web application to check if a website is vulnerable to clickjacking attacks.
"""

import requests
from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import os

app = Flask(__name__)

def normalize_url(url: str) -> str:
    """Normalize URL by adding scheme if missing."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def check_clickjacking(url: str) -> dict:
    """
    Check if a website is vulnerable to clickjacking.

    Returns a dict with:
    - vulnerable: bool indicating if site is vulnerable
    - headers: dict of security headers found
    - message: explanation of the result
    """
    url = normalize_url(url)
    result = {
        'url': url,
        'vulnerable': True,
        'headers': {},
        'message': ''
    }

    try:
        response = requests.get(url)
        headers = response.headers

        result['headers'] = dict(headers)

        x_frame_options = headers.get('X-Frame-Options', None)
        if x_frame_options:
            result['vulnerable'] = x_frame_options.lower() != 'deny'
            result['message'] = f"X-Frame-Options: {x_frame_options}"
        else:
            result['vulnerable'] = True
            result['message'] = "No X-Frame-Options header found."

    except requests.exceptions.ConnectionError:
        result['message'] = 'Connection Error: Tidak dapat terhubung ke website'
    except requests.exceptions.RequestException as e:
        result['message'] = f'Request Error: {str(e)}'
    except Exception as e:
        result['message'] = f'Error: {str(e)}'

    return result

@app.route('/')
def index():
    """Render the main page."""
    return "API Clickjacking Checker Running"

@app.route('/check', methods=['POST'])
def check():
    """API endpoint to check clickjacking vulnerability."""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL tidak boleh kosong'}), 400
    
    result = check_clickjacking(url)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)

