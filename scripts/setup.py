#!/usr/bin/env python3
"""
Setup script for configuring the GitHub backup tool.

This script helps users set up their environment variables and test the connections.
"""

import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def create_env_file():
    """Create a .env file with environment variables."""
    env_file = Path(__file__).parent.parent / ".env"
    
    print("GitHub Backup Tool Setup")
    print("=" * 30)
    print("\nThis script will help you set up your environment variables.")
    print("You'll need:")
    print("1. A GitHub Personal Access Token")
    print("2. A Dropbox Access Token")
    
    # Get GitHub token
    github_token = input("\nEnter your GitHub Personal Access Token: ").strip()
    if not github_token:
        print("Error: GitHub token is required")
        sys.exit(1)
    
    # Get Dropbox token
    dropbox_token = input("Enter your Dropbox Access Token: ").strip()
    if not dropbox_token:
        print("Error: Dropbox token is required")
        sys.exit(1)
    
    # Get backup folder (optional)
    backup_folder = input("Enter Dropbox backup folder [/Projects]: ").strip()
    if not backup_folder:
        backup_folder = "/Projects"
    
    # Create .env file
    env_content = f"""# GitHub Backup Tool Configuration
GITHUB_TOKEN={github_token}
DROPBOX_ACCESS_TOKEN={dropbox_token}
BACKUP_FOLDER={backup_folder}

# Optional: Specify username if backing up another user's public repos
# GITHUB_USERNAME=

# Optional: Repositories to exclude (comma-separated)
# EXCLUDE_REPOS=repo1,repo2,repo3
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"\n✓ Environment file created: {env_file}")
    return env_file


def test_connections(env_file):
    """Test GitHub and Dropbox connections."""
    print("\nTesting connections...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    github_token = os.getenv('GITHUB_TOKEN')
    dropbox_token = os.getenv('DROPBOX_ACCESS_TOKEN')
    
    # Test GitHub connection
    try:
        from github_backup.github_client import GitHubClient
        github_client = GitHubClient(github_token)
        repos = github_client.get_user_repositories()
        print(f"✓ GitHub connection successful - Found {len(repos)} repositories")
    except Exception as e:
        print(f"✗ GitHub connection failed: {e}")
        return False
    
    # Test Dropbox connection
    try:
        from github_backup.dropbox_client import DropboxClient
        dropbox_client = DropboxClient(dropbox_token)
        print("✓ Dropbox connection successful")
    except Exception as e:
        print(f"✗ Dropbox connection failed: {e}")
        return False
    
    return True


def main():
    """Main setup function."""
    print("Welcome to GitHub Backup Tool Setup!\n")
    
    env_file = Path(__file__).parent.parent / ".env"
    
    if env_file.exists():
        response = input(f".env file already exists. Overwrite? [y/N]: ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            sys.exit(0)
    
    # Create environment file
    env_file = create_env_file()
    
    # Test connections
    if test_connections(env_file):
        print("\n✓ Setup completed successfully!")
        print("\nYou can now use the backup tool:")
        print("  python -m github_backup.cli backup-all")
        print("  python scripts/quick_backup.py")
    else:
        print("\n✗ Setup completed with errors. Please check your tokens.")


if __name__ == '__main__':
    main()
