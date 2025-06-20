#!/usr/bin/env python3
"""
Quick backup script for GitHub repositories.

This script provides a simple way to backup repositories without using the full CLI.
"""

import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from github_backup import BackupManager


def main():
    """Run a quick backup of all repositories."""
    # Load environment variables from .env file if it exists
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    # Get tokens from environment
    github_token = os.getenv('GITHUB_TOKEN')
    dropbox_token = os.getenv('DROPBOX_ACCESS_TOKEN')
    
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is required")
        sys.exit(1)
    
    if not dropbox_token:
        print("Error: DROPBOX_ACCESS_TOKEN environment variable is required")
        sys.exit(1)
    
    # Create backup manager
    backup_manager = BackupManager(
        github_token=github_token,
        dropbox_token=dropbox_token,
        backup_folder="/Projects"
    )
    
    print("Starting backup of all repositories...")
    
    # Backup all repositories
    results = backup_manager.backup_all_repositories()
    
    # Print results
    print("\n" + "="*50)
    print("BACKUP RESULTS")
    print("="*50)
    print(f"Total repositories: {results['total_repos']}")
    print(f"Successful backups: {results['successful_backups']}")
    print(f"Failed backups: {results['failed_backups']}")
    print(f"Skipped repositories: {results['skipped_repos']}")
    
    if results['failed_backups'] > 0:
        print("\nFailed repositories:")
        for detail in results['backup_details']:
            if not detail['success']:
                print(f"  - {detail['repo_name']}")
    
    print("\nBackup completed!")


if __name__ == '__main__':
    main()
