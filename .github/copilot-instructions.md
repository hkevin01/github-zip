<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# GitHub Backup Tool - Copilot Instructions

This is a Python project for backing up GitHub repositories to Dropbox. The project uses a src-layout structure and follows modern Python packaging practices.

## Project Structure

- `src/github_backup/`: Main Python package
- `scripts/`: Utility scripts for setup and quick operations
- `docs/`: Project documentation
- `tests/`: Unit tests
- `.github/`: GitHub workflows and templates
- `.copilot/`: Copilot configuration

## Key Components

- `BackupManager`: Main orchestrator for backup operations
- `GitHubClient`: GitHub API client using requests
- `DropboxClient`: Dropbox API client using official dropbox library
- `cli.py`: Click-based command-line interface

## Dependencies

- `requests`: For GitHub API calls
- `dropbox`: Official Dropbox SDK
- `click`: For CLI interface
- `python-dotenv`: For environment variable management

## Coding Standards

- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Use dataclasses for data structures where appropriate
- Include comprehensive docstrings with parameter and return type documentation
- Use pathlib.Path for file system operations
- Handle exceptions gracefully with proper logging

## Testing

- Use pytest for unit tests
- Mock external API calls in tests
- Test both success and failure scenarios
- Include integration tests for full backup workflows

## CLI Patterns

- Use Click decorators for command definition
- Include help text for all commands and options
- Support both environment variables and CLI flags
- Provide clear error messages and exit codes

## Error Handling

- Use specific exception types where possible
- Log errors with appropriate severity levels
- Provide user-friendly error messages
- Continue processing other items when one fails (where appropriate)

## Security

- Never log or expose API tokens
- Use environment variables for sensitive configuration
- Validate input parameters to prevent injection attacks
- Handle rate limiting for API calls

When generating code:

1. Follow the existing code patterns and architecture
2. Include proper error handling and logging
3. Add type hints and docstrings
4. Consider rate limiting and API quotas
5. Use the established project structure and naming conventions
