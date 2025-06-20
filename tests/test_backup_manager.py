"""Tests for backup manager."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from github_backup.backup_manager import BackupManager
from github_backup.github_client import Repository


@pytest.fixture
def sample_repository():
    """Create a sample repository for testing."""
    return Repository(
        name="test-repo",
        full_name="user/test-repo",
        clone_url="https://github.com/user/test-repo.git",
        default_branch="main",
        private=False,
        size=1024,
        updated_at="2023-01-01T00:00:00Z"
    )


@pytest.fixture
def backup_manager():
    """Create a backup manager for testing."""
    with patch('github_backup.backup_manager.GitHubClient'), \
         patch('github_backup.backup_manager.DropboxClient'):
        return BackupManager("fake-github-token", "fake-dropbox-token")


class TestBackupManager:
    """Test cases for BackupManager."""
    
    def test_init(self):
        """Test BackupManager initialization."""
        with patch('github_backup.backup_manager.GitHubClient') as mock_github, \
             patch('github_backup.backup_manager.DropboxClient') as mock_dropbox:
            
            manager = BackupManager("github-token", "dropbox-token", "/CustomFolder")
            
            mock_github.assert_called_once_with("github-token")
            mock_dropbox.assert_called_once_with("dropbox-token")
            assert manager.backup_folder == "/CustomFolder"
    
    def test_backup_all_repositories_success(self, backup_manager, sample_repository):
        """Test successful backup of all repositories."""
        # Mock GitHub client
        backup_manager.github_client.get_user_repositories.return_value = [sample_repository]
        
        # Mock backup_repository method
        with patch.object(backup_manager, 'backup_repository', return_value=True):
            results = backup_manager.backup_all_repositories()
        
        assert results['total_repos'] == 1
        assert results['successful_backups'] == 1
        assert results['failed_backups'] == 0
        assert results['skipped_repos'] == 0
        assert len(results['backup_details']) == 1
        
        detail = results['backup_details'][0]
        assert detail['repo_name'] == 'test-repo'
        assert detail['success'] is True
    
    def test_backup_all_repositories_with_exclusions(self, backup_manager, sample_repository):
        """Test backup with excluded repositories."""
        backup_manager.github_client.get_user_repositories.return_value = [sample_repository]
        
        results = backup_manager.backup_all_repositories(exclude_repos=['test-repo'])
        
        assert results['total_repos'] == 1
        assert results['successful_backups'] == 0
        assert results['failed_backups'] == 0
        assert results['skipped_repos'] == 1
    
    def test_backup_all_repositories_exclude_private(self, backup_manager):
        """Test backup excluding private repositories."""
        private_repo = Repository(
            name="private-repo",
            full_name="user/private-repo",
            clone_url="https://github.com/user/private-repo.git",
            default_branch="main",
            private=True,
            size=512,
            updated_at="2023-01-01T00:00:00Z"
        )
        
        backup_manager.github_client.get_user_repositories.return_value = [private_repo]
        
        results = backup_manager.backup_all_repositories(include_private=False)
        
        assert results['total_repos'] == 1
        assert results['successful_backups'] == 0
        assert results['failed_backups'] == 0
        assert results['skipped_repos'] == 1
    
    @patch('subprocess.run')
    @patch('zipfile.ZipFile')
    @patch('tempfile.TemporaryDirectory')
    def test_backup_repository_success(self, mock_temp_dir, mock_zipfile, mock_subprocess, 
                                     backup_manager, sample_repository):
        """Test successful repository backup."""
        # Mock temporary directory
        mock_temp_dir.return_value.__enter__.return_value = "/tmp/test"
        
        # Mock successful git clone
        mock_subprocess.return_value.returncode = 0
        
        # Mock zip file creation
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        # Mock Dropbox operations
        backup_manager.dropbox_client.create_folder.return_value = True
        backup_manager.dropbox_client.upload_file.return_value = True
        
        # Mock Path.rglob to return some files
        with patch('pathlib.Path.rglob') as mock_rglob:
            mock_file = Mock()
            mock_file.is_file.return_value = True
            mock_file.relative_to.return_value = "file.txt"
            mock_rglob.return_value = [mock_file]
            
            result = backup_manager.backup_repository(sample_repository)
        
        assert result is True
        backup_manager.dropbox_client.create_folder.assert_called_once()
        backup_manager.dropbox_client.upload_file.assert_called_once()
    
    @patch('subprocess.run')
    def test_backup_repository_clone_failure(self, mock_subprocess, backup_manager, sample_repository):
        """Test repository backup with clone failure."""
        # Mock failed git clone
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = "Clone failed"
        
        with patch('tempfile.TemporaryDirectory') as mock_temp_dir:
            mock_temp_dir.return_value.__enter__.return_value = "/tmp/test"
            
            result = backup_manager.backup_repository(sample_repository)
        
        assert result is False
    
    def test_backup_specific_repositories_success(self, backup_manager, sample_repository):
        """Test backup of specific repositories."""
        backup_manager.github_client.get_user_repositories.return_value = [sample_repository]
        
        with patch.object(backup_manager, 'backup_repository', return_value=True):
            results = backup_manager.backup_specific_repositories(['test-repo'])
        
        assert results['requested_repos'] == 1
        assert results['successful_backups'] == 1
        assert results['failed_backups'] == 0
        assert results['not_found_repos'] == 0
    
    def test_backup_specific_repositories_not_found(self, backup_manager):
        """Test backup of non-existent repositories."""
        backup_manager.github_client.get_user_repositories.return_value = []
        
        results = backup_manager.backup_specific_repositories(['nonexistent-repo'])
        
        assert results['requested_repos'] == 1
        assert results['successful_backups'] == 0
        assert results['failed_backups'] == 0
        assert results['not_found_repos'] == 1
