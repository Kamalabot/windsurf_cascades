from flask import render_template, request, jsonify, redirect, url_for, session
from app import app
from app.services.youtube_service import YouTubeService
from app.utils.auth_utils import AuthUtils
from app.utils.file_utils import FileUtils
import os
from urllib.parse import urljoin

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Render the main upload page"""
    # Add debug print
    print("Auth params:", {
        'success': request.args.get('auth_success'),
        'error': request.args.get('auth_error')
    })
    return render_template('index.html', 
                         auth_success=request.args.get('auth_success'),
                         auth_error=request.args.get('auth_error'))

@app.route('/auth')
def auth():
    """Handle OAuth2 authorization initiation"""
    flow = AuthUtils.create_auth_flow(
        'client_secrets.json',
        'http://localhost:7369/oauth2callback'
    )
    authorization_url, state = AuthUtils.get_authorization_url(flow)
    session['state'] = state
    print("Authorization URL:", "reaching here")
    print("Authorization URL:", authorization_url)
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    """Handle OAuth2 callback"""
    try:
        # Verify state to prevent CSRF
        state = session.get('state')
        if not state or state != request.args.get('state', ''):
            return "Invalid state parameter. Possible CSRF attack.", 400

        # Create flow with correct redirect URI
        flow = AuthUtils.create_auth_flow(
            'client_secrets.json',
            'http://localhost:7369/oauth2callback'
        )
        
        # Ensure we have a proper authorization response URL
        if not request.url.startswith('http://'):
            base_url = 'http://localhost:7369'
            authorization_response = urljoin(base_url, request.url)
            print("if not request.url.startswith:", "going here")
        else:
            authorization_response = request.url

        print("oauth2callback:", "reaching here")
        # Exchange authorization code for credentials
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        session['credentials'] = AuthUtils.credentials_to_dict(credentials)
        print("Credentials:", session['credentials']) 
    

        # Debug print before redirect
        print("Redirecting with auth success")
        return redirect(url_for('index', auth_success='true', _scheme='http', _external=True))
    except Exception as e:
        print(f"OAuth callback error: {str(e)}")
        return redirect(url_for('index', auth_error=str(e), _scheme='http', _external=True))

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handle video upload to YouTube"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    video_file = request.files['video']
    success, filepath = FileUtils.save_file_safely(video_file, UPLOAD_FOLDER)
    
    if not success:
        return jsonify({'error': filepath}), 400

    try:
        credentials = AuthUtils.dict_to_credentials(session['credentials'])
        youtube_service = YouTubeService(credentials)
        
        metadata = {
            'title': request.form.get('title', 'Uploaded Video'),
            'description': request.form.get('description', ''),
            'privacy_status': request.form.get('privacy', 'private'),
            'tags': request.form.get('tags', '').split(',') if request.form.get('tags') else []
        }

        response = youtube_service.upload_video(filepath, metadata)
        FileUtils.cleanup_temp_file(filepath)
        
        return jsonify({
            'success': True,
            'video_id': response['id']
        })

    except Exception as e:
        FileUtils.cleanup_temp_file(filepath)
        return jsonify({'error': str(e)}), 500

@app.route('/upload-status/<video_id>')
def upload_status(video_id):
    """Get the status of an uploaded video"""
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        credentials = AuthUtils.dict_to_credentials(session['credentials'])
        youtube_service = YouTubeService(credentials)
        status = youtube_service.get_video_status(video_id)
        
        if not status:
            return jsonify({'error': 'Video not found'}), 404

        return jsonify({'status': status})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth-status')
def auth_status():
    """Check if user is authenticated"""
    try:
        if 'credentials' not in session:
            print({'authenticated': False})
            return jsonify({'authenticated': False})
            
        credentials = AuthUtils.dict_to_credentials(session['credentials'])
        if not credentials or not credentials.valid:
            print({'authenticated due to no credentials': False})
            return jsonify({'authenticated': False})
            
        print({'authenticated': True})
        return jsonify({
            'authenticated': True,
            'email': credentials.id_token.get('email') if credentials.id_token else None
        })
    except Exception as e:
        print(f"Auth status error: {str(e)}")
        return jsonify({'authenticated': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)