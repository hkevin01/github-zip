"""GitHub API client for repository operations."""

import os
import logging
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Repository:
    """Represents a GitHub repository."""
    name: str
    full_name: str
    clone_url: str
    default_branch: str
    private: bool
    size: int
    updated_at: str


class GitHubClient:
    """Client for interacting with GitHub API."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client.
        
        Args:
            token: GitHub personal access token. If None, uses GITHUB_TOKEN env var.
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN env var or pass token parameter.")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'github-backup-tool'
        })
        
        self.base_url = 'https://api.github.com'
        self.logger = logging.getLogger(__name__)
    
    def get_user_repositories(self, username: Optional[str] = None) -> List[Repository]:
        """Get all repositories for a user.
        
        Args:
            username: GitHub username. If None, gets authenticated user's repos.
            
        Returns:
            List of Repository objects.
        """
        if username:
            url = f"{self.base_url}/users/{username}/repos"
        else:
            url = f"{self.base_url}/user/repos"
        
        repos = []
        page = 1
        
        while True:
            response = self.session.get(url, params={
                'page': page,
                'per_page': 100,
                'sort': 'updated',
                'direction': 'desc'
            })
            response.raise_for_status()
            
            data = response.json()
            if not data:
                break
            
            for repo_data in data:
                repo = Repository(
                    name=repo_data['name'],
                    full_name=repo_data['full_name'],
                    clone_url=repo_data['clone_url'],
                    default_branch=repo_data['default_branch'],
                    private=repo_data['private'],
                    size=repo_data['size'],
                    updated_at=repo_data['updated_at']
                )
                repos.append(repo)
            
            page += 1
        
        self.logger.info(f"Found {len(repos)} repositories")
        return repos
    
    def get_repository(self, owner: str, repo_name: str) -> Repository:
        """Get a specific repository.
        
        Args:
            owner: Repository owner username.
            repo_name: Repository name.
            
        Returns:
            Repository object.
        """
        url = f"{self.base_url}/repos/{owner}/{repo_name}"
        response = self.session.get(url)
        response.raise_for_status()
        
        repo_data = response.json()
        return Repository(
            name=repo_data['name'],
            full_name=repo_data['full_name'],
            clone_url=repo_data['clone_url'],
            default_branch=repo_data['default_branch'],
            private=repo_data['private'],
            size=repo_data['size'],
            updated_at=repo_data['updated_at']
        )
