import os
import sys
import importlib

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from App import app
except ImportError as e:
    print(f"Import error: {e}")
    print("Available files:", [f for f in os.listdir('.') if f.endswith('.py')])
    # Create a simple Flask app as fallback
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Flask app is working!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
