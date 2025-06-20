"""Tests for GitHub client."""

import pytest
from unittest.mock import Mock, patch
from github_backup.github_client import GitHubClient, Repository


@pytest.fixture
def github_client():
    """Create a GitHub client for testing."""
    return GitHubClient("fake-token")


@pytest.fixture
def sample_repo_data():
    """Sample repository data from GitHub API."""
    return {
        'name': 'test-repo',
        'full_name': 'user/test-repo',
        'clone_url': 'https://github.com/user/test-repo.git',
        'default_branch': 'main',
        'private': False,
        'size': 1024,
        'updated_at': '2023-01-01T00:00:00Z'
    }


class TestGitHubClient:
    """Test cases for GitHubClient."""
    
    def test_init_with_token(self):
        """Test initialization with token."""
        client = GitHubClient("test-token")
        assert client.token == "test-token"
        assert "token test-token" in client.session.headers['Authorization']
    
    def test_init_without_token_raises_error(self):
        """Test initialization without token raises ValueError."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="GitHub token is required"):
                GitHubClient()
    
    def test_init_with_env_token(self):
        """Test initialization with environment variable token."""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'env-token'}):
            client = GitHubClient()
            assert client.token == "env-token"
    
    def test_get_user_repositories_success(self, github_client, sample_repo_data):
        """Test successful repository retrieval."""
        with patch.object(github_client.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [sample_repo_data]
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            repos = github_client.get_user_repositories()
            
            assert len(repos) == 1
            repo = repos[0]
            assert repo.name == 'test-repo'
            assert repo.full_name == 'user/test-repo'
            assert repo.private is False
            assert repo.size == 1024
    
    def test_get_user_repositories_with_username(self, github_client, sample_repo_data):
        """Test repository retrieval for specific user."""
        with patch.object(github_client.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [sample_repo_data]
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            repos = github_client.get_user_repositories("testuser")
            
            mock_get.assert_called_with(
                "https://api.github.com/users/testuser/repos",
                params={'page': 1, 'per_page': 100, 'sort': 'updated', 'direction': 'desc'}
            )
            assert len(repos) == 1
    
    def test_get_user_repositories_pagination(self, github_client, sample_repo_data):
        """Test repository retrieval with pagination."""
        with patch.object(github_client.session, 'get') as mock_get:
            # First page response
            first_response = Mock()
            first_response.json.return_value = [sample_repo_data]
            first_response.raise_for_status.return_value = None
            
            # Second page response (empty)
            second_response = Mock()
            second_response.json.return_value = []
            second_response.raise_for_status.return_value = None
            
            mock_get.side_effect = [first_response, second_response]
            
            repos = github_client.get_user_repositories()
            
            assert len(repos) == 1
            assert mock_get.call_count == 2
    
    def test_get_repository_success(self, github_client, sample_repo_data):
        """Test successful single repository retrieval."""
        with patch.object(github_client.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = sample_repo_data
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            repo = github_client.get_repository("user", "test-repo")
            
            mock_get.assert_called_with("https://api.github.com/repos/user/test-repo")
            assert repo.name == 'test-repo'
            assert repo.full_name == 'user/test-repo'
    
    def test_get_repository_not_found(self, github_client):
        """Test repository not found error."""
        with patch.object(github_client.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = Exception("404 Not Found")
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception, match="404 Not Found"):
                github_client.get_repository("user", "nonexistent-repo")


class TestRepository:
    """Test cases for Repository dataclass."""
    
    def test_repository_creation(self):
        """Test Repository object creation."""
        repo = Repository(
            name="test-repo",
            full_name="user/test-repo",
            clone_url="https://github.com/user/test-repo.git",
            default_branch="main",
            private=False,
            size=1024,
            updated_at="2023-01-01T00:00:00Z"
        )
        
        assert repo.name == "test-repo"
        assert repo.full_name == "user/test-repo"
        assert repo.clone_url == "https://github.com/user/test-repo.git"
        assert repo.default_branch == "main"
        assert repo.private is False
        assert repo.size == 1024
        assert repo.updated_at == "2023-01-01T00:00:00Z"
