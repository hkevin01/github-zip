# Configuration Guide

## Environment Variables

The GitHub Backup Tool uses environment variables for configuration. You can set these in a `.env` file or export them in your shell.

### Required Variables

#### GITHUB_TOKEN
Your GitHub Personal Access Token.

**How to get it:**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Select the following scopes:
   - `repo` (for private repositories)
   - `public_repo` (for public repositories)
4. Copy the generated token

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### DROPBOX_ACCESS_TOKEN
Your Dropbox Access Token.

**How to get it:**
1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Click "Create app"
3. Choose "Scoped access"
4. Choose "Full Dropbox" access
5. Name your app (e.g., "GitHub Backup Tool")
6. Go to the app settings
7. In the "OAuth 2" section, click "Generate access token"
8. Copy the generated token

```env
DROPBOX_ACCESS_TOKEN=sl.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Optional Variables

#### BACKUP_FOLDER
Dropbox folder where backups will be stored.

Default: `/Projects`

```env
BACKUP_FOLDER=/MyBackups
```

#### GITHUB_USERNAME
Default GitHub username to use when not specified.

```env
GITHUB_USERNAME=your-username
```

#### EXCLUDE_REPOS
Comma-separated list of repository names to exclude from backups.

```env
EXCLUDE_REPOS=repo1,repo2,temp-project
```

## Configuration File

You can also create a configuration file at `~/.github-backup/config.ini`:

```ini
[github]
token = ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
username = your-username

[dropbox]
token = sl.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
backup_folder = /Projects

[backup]
exclude_repos = repo1,repo2,temp-project
include_private = true
```

## CLI Configuration

You can override any configuration using CLI flags:

```bash
# Override tokens
github-backup backup-all --github-token YOUR_TOKEN --dropbox-token YOUR_TOKEN

# Override backup folder
github-backup backup-all --backup-folder /MyBackups

# Override username
github-backup backup-all --username other-user

# Exclude repositories
github-backup backup-all --exclude repo1 --exclude repo2
```

## Dropbox Folder Structure

The tool organizes backups in the following structure:

```
/Projects/                          # Root backup folder
├── repository1/                    # One folder per repository
│   ├── repository1_20231201_120000.zip
│   ├── repository1_20231202_130000.zip
│   └── repository1_20231203_140000.zip
├── repository2/
│   ├── repository2_20231201_120000.zip
│   └── repository2_20231202_130000.zip
└── private-repo/
    └── private-repo_20231201_120000.zip
```

### Filename Format

Backup files use the following naming convention:
```
{repository_name}_{YYYYMMDD}_{HHMMSS}.zip
```

Where:
- `repository_name`: The GitHub repository name
- `YYYYMMDD`: Date in year-month-day format
- `HHMMSS`: Time in hour-minute-second format (24-hour)

## Security Considerations

### Token Storage
- Store tokens in environment variables or `.env` files
- Never commit tokens to version control
- Use `.gitignore` to exclude `.env` files
- Consider using a password manager for token storage

### Token Permissions
- Use minimal required permissions for GitHub tokens
- For public repositories only: use `public_repo` scope
- For private repositories: use `repo` scope
- Regularly rotate your tokens

### Dropbox Security
- Use app-specific access tokens
- Limit app permissions to necessary folders
- Monitor app activity in Dropbox settings

## Troubleshooting Configuration

### Invalid GitHub Token
```
Error: GitHub token is required
```

**Solutions:**
1. Check if `GITHUB_TOKEN` is set in your environment
2. Verify the token is valid by testing it manually
3. Check token permissions include required scopes

### Invalid Dropbox Token
```
Error: Invalid Dropbox access token
```

**Solutions:**
1. Check if `DROPBOX_ACCESS_TOKEN` is set
2. Verify the token hasn't expired
3. Check if the app has necessary permissions

### Permission Denied
```
Error: Repository not found or access denied
```

**Solutions:**
1. Check if you have access to the repository
2. For private repositories, ensure token has `repo` scope
3. Verify the repository name is correct

### Dropbox Storage Full
```
Error: Insufficient storage space
```

**Solutions:**
1. Check your Dropbox storage quota
2. Clean up old backups
3. Upgrade your Dropbox plan if needed
