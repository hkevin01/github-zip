"""GitHub Repository Backup Tool

A Python package for backing up GitHub repositories to Dropbox.
"""

__version__ = "0.1.0"
__author__ = "Kevin"
__email__ = ""

from .backup_manager import BackupManager
from .github_client import GitHubClient
from .dropbox_client import DropboxClient

__all__ = ["BackupManager", "GitHubClient", "DropboxClient"]
