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
        'message': 'Welcome to Techkedgeconnect - Learn Modern Application Deployment and Observability',
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
    # Hardcoded values for host, port, and debug mode
    host = '0.0.0.0'  # The app will be accessible on all network interfaces
    port = 5000       # The port to run the application on
    debug_mode = False  # Set debug mode to False

    # Log the startup message
    app.logger.info(f"Starting app on {host}:{port} with debug={debug_mode}")

    # Start the Flask app
    app.run(host=host, port=port, debug=debug_mode)

