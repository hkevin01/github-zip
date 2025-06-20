# GitHub Backup Tool

A Python tool for backing up GitHub repositories to Dropbox. This tool clones your repositories, creates zip archives, and uploads them to your Dropbox account for safekeeping.

## Features

- ✅ Backup all repositories for a user (public and private)
- ✅ Backup specific repositories by name
- ✅ Mirror cloning preserves full git history
- ✅ Automatic zip compression
- ✅ Upload to organized Dropbox folders
- ✅ CLI interface with multiple commands
- ✅ Environment variable configuration
- ✅ Detailed logging and error handling
- ✅ Progress tracking and results reporting

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/github-backup.git
cd github-backup

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### 2. Setup

Run the setup script to configure your API tokens:

```bash
python scripts/setup.py
```

This will prompt you for:
- GitHub Personal Access Token
- Dropbox Access Token
- Backup folder path (default: `/Projects`)

### 3. Basic Usage

```bash
# Backup all your repositories
github-backup backup-all

# Backup specific repositories
github-backup backup-repos repo1 repo2 repo3

# List your repositories
github-backup list-repos

# Quick backup with script
python scripts/quick_backup.py
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token_here
DROPBOX_ACCESS_TOKEN=your_dropbox_token_here
BACKUP_FOLDER=/Projects
```

### Getting API Tokens

#### GitHub Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Copy the token and add it to your `.env` file

#### Dropbox Access Token
1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Create a new app with "Full Dropbox" access
3. Generate an access token
4. Copy the token and add it to your `.env` file

## CLI Usage

### Backup All Repositories

```bash
# Backup all repositories for authenticated user
github-backup backup-all

# Backup for specific user (public repos only)
github-backup backup-all --username other-user

# Exclude specific repositories
github-backup backup-all --exclude repo1 --exclude repo2

# Include only public repositories
github-backup backup-all --no-private

# Custom backup folder
github-backup backup-all --backup-folder /MyBackups

# Save results to file
github-backup backup-all --output results.json
```

### Backup Specific Repositories

```bash
# Backup specific repositories
github-backup backup-repos repo1 repo2 repo3

# Backup from specific user
github-backup backup-repos repo1 repo2 --username other-user
```

### List Repositories

```bash
# List your repositories
github-backup list-repos

# List another user's repositories
github-backup list-repos --username other-user
```

## Python API

You can also use the tool programmatically:

```python
from github_backup import BackupManager

# Initialize backup manager
backup_manager = BackupManager(
    github_token="your_token",
    dropbox_token="your_token",
    backup_folder="/Projects"
)

# Backup all repositories
results = backup_manager.backup_all_repositories()

# Backup specific repositories
results = backup_manager.backup_specific_repositories(['repo1', 'repo2'])

print(f"Successful backups: {results['successful_backups']}")
print(f"Failed backups: {results['failed_backups']}")
```

## Project Structure

```
github-backup/
├── src/
│   └── github_backup/
│       ├── __init__.py
│       ├── backup_manager.py    # Main backup logic
│       ├── github_client.py     # GitHub API client
│       ├── dropbox_client.py    # Dropbox API client
│       └── cli.py              # Command-line interface
├── scripts/
│   ├── quick_backup.py         # Simple backup script
│   ├── setup.py               # Environment setup
│   └── dev_setup.sh           # Development environment setup
├── docs/                      # Documentation
├── tests/                     # Unit tests
├── .github/                   # GitHub workflows and templates
├── .copilot/                  # Copilot configuration
├── pyproject.toml            # Project configuration
├── requirements.txt          # Runtime dependencies
└── requirements-dev.txt      # Development dependencies
```

## Development

### Setup Development Environment

```bash
# Run development setup script
./scripts/dev_setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
pre-commit install
```

### Code Quality

```bash
# Format code
black src/ scripts/ tests/
isort src/ scripts/ tests/

# Lint code
flake8 src/ scripts/ tests/
mypy src/

# Run tests
pytest
pytest --cov=src/github_backup
```

## How It Works

1. **Authentication**: Uses GitHub Personal Access Token and Dropbox Access Token
2. **Repository Discovery**: Fetches repository list via GitHub API
3. **Cloning**: Uses `git clone --mirror` to create bare repository clones
4. **Compression**: Creates zip archives of the cloned repositories
5. **Upload**: Uploads zip files to Dropbox in organized folder structure
6. **Cleanup**: Removes temporary files after successful upload

## Backup Structure

Repositories are organized in Dropbox as:

```
/Projects/
├── repo1/
│   ├── repo1_20231201_120000.zip
│   └── repo1_20231202_130000.zip
├── repo2/
│   └── repo2_20231201_120000.zip
└── repo3/
    └── repo3_20231201_120000.zip
```

## Troubleshooting

### Common Issues

1. **"GitHub token is required"**
   - Make sure your `.env` file contains `GITHUB_TOKEN=your_token`
   - Or pass the token with `--github-token` flag

2. **"Dropbox access token is required"**
   - Make sure your `.env` file contains `DROPBOX_ACCESS_TOKEN=your_token`
   - Or pass the token with `--dropbox-token` flag

3. **"Failed to clone repository"**
   - Check your internet connection
   - Verify you have access to the repository
   - Check if the repository URL is correct

4. **"Upload failed"**
   - Check your Dropbox storage space
   - Verify the Dropbox token has write permissions
   - Check network connectivity

### Logs

Enable verbose logging with the `-v` flag:

```bash
github-backup -v backup-all
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

## Support

- 📖 Documentation: [docs/](docs/)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/github-backup/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/github-backup/discussions)
