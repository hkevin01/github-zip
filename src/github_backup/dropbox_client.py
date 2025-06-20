"""Dropbox client for file upload operations."""

import os
import logging
from typing import Optional
import dropbox
from dropbox.exceptions import AuthError, ApiError


class DropboxClient:
    """Client for interacting with Dropbox API."""
    
    def __init__(self, access_token: Optional[str] = None):
        """Initialize Dropbox client.
        
        Args:
            access_token: Dropbox access token. If None, uses DROPBOX_ACCESS_TOKEN env var.
        """
        self.access_token = access_token or os.getenv('DROPBOX_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("Dropbox access token is required. Set DROPBOX_ACCESS_TOKEN env var or pass token parameter.")
        
        self.client = dropbox.Dropbox(self.access_token)
        self.logger = logging.getLogger(__name__)
        
        # Test connection
        try:
            self.client.users_get_current_account()
            self.logger.info("Successfully connected to Dropbox")
        except AuthError as e:
            raise ValueError(f"Invalid Dropbox access token: {e}")
    
    def upload_file(self, local_path: str, dropbox_path: str, overwrite: bool = True) -> bool:
        """Upload a file to Dropbox.
        
        Args:
            local_path: Path to local file.
            dropbox_path: Destination path in Dropbox.
            overwrite: Whether to overwrite existing files.
            
        Returns:
            True if upload successful, False otherwise.
        """
        try:
            with open(local_path, 'rb') as f:
                file_size = os.path.getsize(local_path)
                
                if file_size <= 150 * 1024 * 1024:  # 150MB - use simple upload
                    mode = dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add
                    self.client.files_upload(f.read(), dropbox_path, mode=mode)
                else:
                    # Use upload session for large files
                    self._upload_large_file(f, dropbox_path, file_size, overwrite)
                
                self.logger.info(f"Successfully uploaded {local_path} to {dropbox_path}")
                return True
                
        except FileNotFoundError:
            self.logger.error(f"Local file not found: {local_path}")
            return False
        except ApiError as e:
            self.logger.error(f"Dropbox API error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error uploading file: {e}")
            return False
    
    def _upload_large_file(self, file_obj, dropbox_path: str, file_size: int, overwrite: bool):
        """Upload large file using upload session."""
        CHUNK_SIZE = 4 * 1024 * 1024  # 4MB chunks
        
        session_start_result = self.client.files_upload_session_start(file_obj.read(CHUNK_SIZE))
        cursor = dropbox.files.UploadSessionCursor(
            session_id=session_start_result.session_id,
            offset=file_obj.tell()
        )
        
        while file_obj.tell() < file_size:
            remaining = file_size - file_obj.tell()
            chunk_size = min(CHUNK_SIZE, remaining)
            
            if remaining <= CHUNK_SIZE:
                # Last chunk
                mode = dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add
                commit = dropbox.files.CommitInfo(path=dropbox_path, mode=mode)
                self.client.files_upload_session_finish(
                    file_obj.read(chunk_size), cursor, commit
                )
                break
            else:
                self.client.files_upload_session_append_v2(
                    file_obj.read(chunk_size), cursor
                )
                cursor.offset = file_obj.tell()
    
    def create_folder(self, path: str) -> bool:
        """Create a folder in Dropbox.
        
        Args:
            path: Folder path to create.
            
        Returns:
            True if folder created or already exists, False otherwise.
        """
        try:
            self.client.files_create_folder_v2(path)
            self.logger.info(f"Created folder: {path}")
            return True
        except ApiError as e:
            if e.error.is_path() and e.error.get_path().is_conflict():
                # Folder already exists
                self.logger.info(f"Folder already exists: {path}")
                return True
            else:
                self.logger.error(f"Error creating folder {path}: {e}")
                return False
    
    def file_exists(self, path: str) -> bool:
        """Check if a file exists in Dropbox.
        
        Args:
            path: File path to check.
            
        Returns:
            True if file exists, False otherwise.
        """
        try:
            self.client.files_get_metadata(path)
            return True
        except ApiError:
            return False
