import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Route for the index page
@app.route('/')
def index():
    app.logger.info("Index route accessed")
    return jsonify({
        'message': 'Welcome to Surfing in Canada',
    })

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning("404 error occurred: %s", e)
    return jsonify({"error": "Page not found"}), 404

# Custom 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error("500 error occurred: %s", e)
    return jsonify({"error": "Internal server error"}), 500

# Run the app
if __name__ == '__main__':
    # Use environment variables for host and port
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))

    # Enable debug mode via environment variable, default is False
    debug_mode = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

    # Log the startup message
    app.logger.info(f"Starting app on {host}:{port} with debug={debug_mode}")

    # Start the Flask app
    app.run(host=host, port=port, debug=debug_mode)
