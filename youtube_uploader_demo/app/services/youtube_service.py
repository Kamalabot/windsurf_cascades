from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from typing import Dict, Any, Optional
import os

class YouTubeService:
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self.youtube = build(self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials)

    def upload_video(self, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload a video to YouTube
        
        Args:
            file_path: Path to the video file
            metadata: Dictionary containing video metadata (title, description, privacy)
        
        Returns:
            Dictionary containing upload response
        """
        body = {
            'snippet': {
                'title': metadata.get('title', 'Uploaded Video'),
                'description': metadata.get('description', ''),
                'tags': metadata.get('tags', [])
            },
            'status': {
                'privacyStatus': metadata.get('privacy_status', 'private')
            }
        }

        insert_request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=MediaFileUpload(
                file_path,
                chunksize=-1,
                resumable=True
            )
        )

        return insert_request.execute()

    def get_video_status(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary containing video status or None if not found
        """
        try:
            response = self.youtube.videos().list(
                part='status',
                id=video_id
            ).execute()
            
            return response['items'][0] if response.get('items') else None
        except Exception as e:
            print(f"Error getting video status: {str(e)}")
            return None