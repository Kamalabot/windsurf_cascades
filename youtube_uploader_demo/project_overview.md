# YouTube Video Uploader Application

## Project Overview
A web-based application that allows users to upload multiple videos to YouTube using the YouTube Data API v3. The application features a modern, user-friendly interface for selecting and managing video uploads.

## Key Features
- Multiple video file selection and upload
- YouTube API integration
- Progress tracking for uploads
- Video metadata management (title, description, privacy settings)
- Responsive and intuitive user interface

## Technical Stack
### Frontend
- HTML5, CSS3, JavaScript
- Modern file upload interface with drag-and-drop functionality
- Bootstrap for responsive design
- Progress bars for upload status

### Backend
- Python with Flask framework
- YouTube Data API v3
- OAuth 2.0 authentication

## Components
1. **Frontend Interface**
   - Multiple file selection component
   - Drag and drop zone
   - Upload progress visualization
   - Form fields for video metadata
   - Responsive design for various screen sizes

2. **Backend Services**
   - YouTube API integration service
   - Authentication handling
   - File upload management
   - Video metadata processing

3. **API Integration**
   - YouTube Data API v3 implementation
   - OAuth 2.0 flow for authentication
   - Chunked upload support for large files

## Security Considerations
- Secure handling of OAuth credentials
- Environment-based configuration
- Input validation and sanitization
- File type validation
- Maximum file size restrictions

## Project Structure
```
youtube_uploader_demo/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/
├── config/
├── app/
│   ├── routes/
│   ├── services/
│   └── utils/
├── requirements.txt
└── README.md
```

## Implementation Phases
1. **Phase 1: Setup and Basic Structure**
   - Project initialization
   - Dependencies setup
   - Basic folder structure

2. **Phase 2: Frontend Development**
   - HTML/CSS structure
   - File upload interface
   - Form components

3. **Phase 3: Backend Development**
   - Flask server setup
   - YouTube API integration
   - File handling implementation

4. **Phase 4: Integration and Testing**
   - Frontend-backend integration
   - Upload functionality testing
   - Error handling implementation

## Dependencies
- Flask
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2
- python-dotenv
## Google API Key Generation Process
1. **Create a Google Cloud Project**
   - Go to the Google Cloud Console (https://console.cloud.google.com/)
   - Click on "Select a project" > "New Project"
   - Name your project and click "Create"

2. **Enable YouTube Data API v3**
   - In the Cloud Console, go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3" and click on it
   - Click "Enable"

3. **Create Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Web application" as the application type
   - Set up authorized JavaScript origins and redirect URIs
   - Download the client configuration file

4. **Set Up OAuth Consent Screen**
   - Go to "OAuth consent screen" in the left sidebar
   - Choose "External" user type (unless your app is for internal use only)
   - Fill in the required information about your app

5. **Configure Environment Variables**
   - Store your client ID, client secret, and API key in environment variables
   - Use these variables in your application configuration

6. **Implement OAuth 2.0 Flow**
   - Use the Google Auth Library to implement the OAuth 2.0 flow in your application
   - Ensure proper token storage and refresh mechanisms

Remember to keep your API credentials secure and never expose them in public repositories or client-side code.

## Configuration Requirements
- YouTube API credentials
- OAuth 2.0 client configuration
- Environment variables setup
- CORS and security settings
