"""Main backup manager for GitHub repositories."""

import os
import shutil
import tempfile
import zipfile
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import subprocess

from .github_client import GitHubClient, Repository
from .dropbox_client import DropboxClient


class BackupManager:
    """Manages the backup process of GitHub repositories to Dropbox."""
    
    def __init__(self, 
                 github_token: Optional[str] = None,
                 dropbox_token: Optional[str] = None,
                 backup_folder: str = "/Projects"):
        """Initialize backup manager.
        
        Args:
            github_token: GitHub personal access token.
            dropbox_token: Dropbox access token.
            backup_folder: Dropbox folder for backups.
        """
        self.github_client = GitHubClient(github_token)
        self.dropbox_client = DropboxClient(dropbox_token)
        self.backup_folder = backup_folder.rstrip('/')
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def backup_all_repositories(self, 
                               username: Optional[str] = None,
                               exclude_repos: List[str] = None,
                               include_private: bool = True) -> Dict[str, Any]:
        """Backup all repositories for a user.
        
        Args:
            username: GitHub username. If None, uses authenticated user.
            exclude_repos: List of repository names to exclude.
            include_private: Whether to include private repositories.
            
        Returns:
            Dictionary with backup results.
        """
        exclude_repos = exclude_repos or []
        results = {
            'total_repos': 0,
            'successful_backups': 0,
            'failed_backups': 0,
            'skipped_repos': 0,
            'backup_details': []
        }
        
        try:
            repos = self.github_client.get_user_repositories(username)
            results['total_repos'] = len(repos)
            
            # Filter repositories
            filtered_repos = []
            for repo in repos:
                if repo.name in exclude_repos:
                    self.logger.info(f"Skipping excluded repository: {repo.name}")
                    results['skipped_repos'] += 1
                    continue
                
                if not include_private and repo.private:
                    self.logger.info(f"Skipping private repository: {repo.name}")
                    results['skipped_repos'] += 1
                    continue
                
                filtered_repos.append(repo)
            
            # Backup each repository
            for repo in filtered_repos:
                self.logger.info(f"Starting backup for repository: {repo.name}")
                success = self.backup_repository(repo)
                
                backup_detail = {
                    'repo_name': repo.name,
                    'full_name': repo.full_name,
                    'success': success,
                    'timestamp': datetime.now().isoformat(),
                    'private': repo.private,
                    'size_kb': repo.size
                }
                results['backup_details'].append(backup_detail)
                
                if success:
                    results['successful_backups'] += 1
                else:
                    results['failed_backups'] += 1
            
            self.logger.info(f"Backup completed. Success: {results['successful_backups']}, "
                           f"Failed: {results['failed_backups']}, "
                           f"Skipped: {results['skipped_repos']}")
            
        except Exception as e:
            self.logger.error(f"Error during backup process: {e}")
            results['error'] = str(e)
        
        return results
    
    def backup_repository(self, repo: Repository) -> bool:
        """Backup a single repository.
        
        Args:
            repo: Repository object to backup.
            
        Returns:
            True if backup successful, False otherwise.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Clone repository
                repo_path = Path(temp_dir) / repo.name
                self.logger.info(f"Cloning repository: {repo.clone_url}")
                
                clone_result = subprocess.run([
                    'git', 'clone', '--mirror', repo.clone_url, str(repo_path)
                ], capture_output=True, text=True, timeout=300)
                
                if clone_result.returncode != 0:
                    self.logger.error(f"Failed to clone {repo.name}: {clone_result.stderr}")
                    return False
                
                # Create zip file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                zip_filename = f"{repo.name}_{timestamp}.zip"
                zip_path = Path(temp_dir) / zip_filename
                
                self.logger.info(f"Creating zip file: {zip_filename}")
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in repo_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(repo_path)
                            zipf.write(file_path, arcname)
                
                # Upload to Dropbox
                dropbox_path = f"{self.backup_folder}/{repo.name}/{zip_filename}"
                
                # Ensure folder exists
                folder_path = f"{self.backup_folder}/{repo.name}"
                self.dropbox_client.create_folder(folder_path)
                
                self.logger.info(f"Uploading to Dropbox: {dropbox_path}")
                success = self.dropbox_client.upload_file(str(zip_path), dropbox_path)
                
                if success:
                    self.logger.info(f"Successfully backed up {repo.name}")
                else:
                    self.logger.error(f"Failed to upload {repo.name} to Dropbox")
                
                return success
                
            except subprocess.TimeoutExpired:
                self.logger.error(f"Timeout while cloning {repo.name}")
                return False
            except Exception as e:
                self.logger.error(f"Error backing up {repo.name}: {e}")
                return False
    
    def backup_specific_repositories(self, repo_names: List[str], username: Optional[str] = None) -> Dict[str, Any]:
        """Backup specific repositories by name.
        
        Args:
            repo_names: List of repository names to backup.
            username: GitHub username. If None, uses authenticated user.
            
        Returns:
            Dictionary with backup results.
        """
        results = {
            'requested_repos': len(repo_names),
            'successful_backups': 0,
            'failed_backups': 0,
            'not_found_repos': 0,
            'backup_details': []
        }
        
        for repo_name in repo_names:
            try:
                if username:
                    repo = self.github_client.get_repository(username, repo_name)
                else:
                    # Get authenticated user's username first
                    all_repos = self.github_client.get_user_repositories()
                    user_repo = next((r for r in all_repos if r.name == repo_name), None)
                    if not user_repo:
                        self.logger.error(f"Repository not found: {repo_name}")
                        results['not_found_repos'] += 1
                        continue
                    repo = user_repo
                
                success = self.backup_repository(repo)
                
                backup_detail = {
                    'repo_name': repo.name,
                    'full_name': repo.full_name,
                    'success': success,
                    'timestamp': datetime.now().isoformat()
                }
                results['backup_details'].append(backup_detail)
                
                if success:
                    results['successful_backups'] += 1
                else:
                    results['failed_backups'] += 1
                    
            except Exception as e:
                self.logger.error(f"Error processing repository {repo_name}: {e}")
                results['failed_backups'] += 1
                backup_detail = {
                    'repo_name': repo_name,
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                results['backup_details'].append(backup_detail)
        
        return results
