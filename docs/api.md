# API Documentation

## BackupManager

The main class for managing repository backups.

### Constructor

```python
BackupManager(github_token=None, dropbox_token=None, backup_folder="/Projects")
```

**Parameters:**
- `github_token` (str, optional): GitHub personal access token
- `dropbox_token` (str, optional): Dropbox access token  
- `backup_folder` (str): Dropbox folder for backups (default: "/Projects")

### Methods

#### backup_all_repositories()

```python
backup_all_repositories(username=None, exclude_repos=None, include_private=True)
```

Backup all repositories for a user.

**Parameters:**
- `username` (str, optional): GitHub username. If None, uses authenticated user
- `exclude_repos` (List[str], optional): Repository names to exclude
- `include_private` (bool): Whether to include private repositories (default: True)

**Returns:**
- `Dict[str, Any]`: Backup results dictionary

#### backup_repository()

```python
backup_repository(repo)
```

Backup a single repository.

**Parameters:**
- `repo` (Repository): Repository object to backup

**Returns:**
- `bool`: True if backup successful, False otherwise

#### backup_specific_repositories()

```python
backup_specific_repositories(repo_names, username=None)
```

Backup specific repositories by name.

**Parameters:**
- `repo_names` (List[str]): Repository names to backup
- `username` (str, optional): GitHub username

**Returns:**
- `Dict[str, Any]`: Backup results dictionary

## GitHubClient

Client for interacting with GitHub API.

### Constructor

```python
GitHubClient(token=None)
```

**Parameters:**
- `token` (str, optional): GitHub personal access token

### Methods

#### get_user_repositories()

```python
get_user_repositories(username=None)
```

Get all repositories for a user.

**Parameters:**
- `username` (str, optional): GitHub username

**Returns:**
- `List[Repository]`: List of Repository objects

#### get_repository()

```python
get_repository(owner, repo_name)
```

Get a specific repository.

**Parameters:**
- `owner` (str): Repository owner username
- `repo_name` (str): Repository name

**Returns:**
- `Repository`: Repository object

## DropboxClient

Client for interacting with Dropbox API.

### Constructor

```python
DropboxClient(access_token=None)
```

**Parameters:**
- `access_token` (str, optional): Dropbox access token

### Methods

#### upload_file()

```python
upload_file(local_path, dropbox_path, overwrite=True)
```

Upload a file to Dropbox.

**Parameters:**
- `local_path` (str): Path to local file
- `dropbox_path` (str): Destination path in Dropbox
- `overwrite` (bool): Whether to overwrite existing files (default: True)

**Returns:**
- `bool`: True if upload successful, False otherwise

#### create_folder()

```python
create_folder(path)
```

Create a folder in Dropbox.

**Parameters:**
- `path` (str): Folder path to create

**Returns:**
- `bool`: True if folder created or exists, False otherwise

#### file_exists()

```python
file_exists(path)
```

Check if a file exists in Dropbox.

**Parameters:**
- `path` (str): File path to check

**Returns:**
- `bool`: True if file exists, False otherwise

## Repository

Data class representing a GitHub repository.

### Attributes

- `name` (str): Repository name
- `full_name` (str): Full repository name (owner/repo)
- `clone_url` (str): Repository clone URL
- `default_branch` (str): Default branch name
- `private` (bool): Whether repository is private
- `size` (int): Repository size in KB
- `updated_at` (str): Last update timestamp

## Results Dictionary

The backup methods return a dictionary with the following structure:

```python
{
    'total_repos': int,           # Total number of repositories
    'successful_backups': int,    # Number of successful backups
    'failed_backups': int,        # Number of failed backups
    'skipped_repos': int,         # Number of skipped repositories
    'backup_details': [           # List of backup details
        {
            'repo_name': str,     # Repository name
            'full_name': str,     # Full repository name
            'success': bool,      # Whether backup was successful
            'timestamp': str,     # Backup timestamp
            'private': bool,      # Whether repository is private
            'size_kb': int        # Repository size in KB
        }
    ]
}
```
