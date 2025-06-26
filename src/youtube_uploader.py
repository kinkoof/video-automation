import os
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json


class YouTubeUploader:
    def __init__(self):
        self.credentials_path = Path(
            __file__).parent.parent / 'config' / 'client_secrets.json'
        self.token_path = Path(__file__).parent.parent / \
            'config' / 'token.pickle'
        # Use escopos mínimos necessários
        self.scopes = [
            'https://www.googleapis.com/auth/youtube.upload',
            'https://www.googleapis.com/auth/youtube'
        ]

        # Permitir aplicativos não verificados durante desenvolvimento
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

        # Load config
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        with open(config_path) as f:
            self.config = json.load(f)

    def get_authenticated_service(self):
        """Get authenticated YouTube service."""
        credentials = None

        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                credentials = pickle.load(token)

        # If credentials are invalid or don't exist, get new ones
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), self.scopes)
                # Use uma porta específica que deve corresponder à configurada no Google Cloud Console
                credentials = flow.run_local_server(
                    port=8080,
                    success_message='Autenticação concluída! Você pode fechar esta janela.'
                )

            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(credentials, token)

        return build('youtube', 'v3', credentials=credentials)

    def upload_video(self, video_path, title, description=None, privacy_status="private"):
        """
        Upload a video to YouTube.

        Args:
            video_path (str): Path to the video file
            title (str): Video title
            description (str, optional): Video description
            privacy_status (str): Privacy status ("private", "unlisted", or "public")

        Returns:
            str: Video ID if successful, None if failed
        """
        try:
            youtube = self.get_authenticated_service()

            if description is None:
                description = "Created with Video Automation"

            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'categoryId': '22'  # People & Blogs category
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }

            # Create MediaFileUpload object
            media = MediaFileUpload(
                video_path,
                chunksize=1024*1024,
                resumable=True
            )

            # Execute upload
            print(f"🎥 Uploading video to YouTube: {title}")
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Uploaded {int(status.progress() * 100)}%")

            print(f"✅ Upload complete! Video ID: {response['id']}")
            return response['id']

        except Exception as e:
            print(f"❌ Error uploading video: {str(e)}")
            return None


if __name__ == "__main__":
    # Test upload
    uploader = YouTubeUploader()
    video_id = uploader.upload_video(
        "output/final_video.mp4",
        "Test Upload",
        "This is a test upload",
        "private"
    )
    if video_id:
        print(f"Video uploaded successfully: https://youtu.be/{video_id}")
