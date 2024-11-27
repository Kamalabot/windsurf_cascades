from app import app
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Enable HTTPS for OAuth
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # For development only
    
    # Enable hot reloading and debugging
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Run on port 7369 to match the redirect URI
    app.run(debug=True, use_reloader=True, port=7369, host='0.0.0.0')