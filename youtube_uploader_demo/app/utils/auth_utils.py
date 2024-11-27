from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from typing import Tuple, Optional
import os
import json

class AuthUtils:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    @staticmethod
    def create_auth_flow(client_secrets_file: str, redirect_uri: str) -> Flow:
        """
        Create OAuth2 flow instance
        """
        return Flow.from_client_secrets_file(
            client_secrets_file,
            scopes=AuthUtils.SCOPES,
            redirect_uri=redirect_uri
        )

    @staticmethod
    def get_authorization_url(flow: Flow) -> Tuple[str, str]:
        """
        Get authorization URL and state
        """
        return flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

    @staticmethod
    def credentials_to_dict(credentials: Credentials) -> dict:
        """
        Convert credentials to dictionary
        """
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

    @staticmethod
    def dict_to_credentials(credentials_dict: dict) -> Optional[Credentials]:
        """
        Convert dictionary to credentials
        """
        try:
            return Credentials(
                token=credentials_dict['token'],
                refresh_token=credentials_dict['refresh_token'],
                token_uri=credentials_dict['token_uri'],
                client_id=credentials_dict['client_id'],
                client_secret=credentials_dict['client_secret'],
                scopes=credentials_dict['scopes']
            )
        except Exception as e:
            print(f"Error creating credentials: {str(e)}")
            return None