# Contributing to GitHub Backup Tool

Thank you for considering contributing to the GitHub Backup Tool! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

1. Use the GitHub issue tracker
2. Use the bug report template
3. Include detailed reproduction steps
4. Remove sensitive information (tokens, usernames)

### Suggesting Features

1. Use the GitHub issue tracker
2. Use the feature request template
3. Describe the problem you're solving
4. Provide specific use cases

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests
5. Update documentation if needed
6. Run the test suite
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub account
- Dropbox developer account (for testing)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/github-backup.git
   cd github-backup
   ```

2. **Run development setup**
   ```bash
   ./scripts/dev_setup.sh
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Set up environment variables**
   ```bash
   python scripts/setup.py
   ```

## Code Standards

### Style Guidelines

- Follow PEP 8
- Use Black for code formatting
- Use isort for import sorting
- Maximum line length: 88 characters
- Use type hints for all functions

### Code Quality Tools

Run these commands before submitting:

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

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Examples:
```
feat(backup): add support for organization backups
fix(cli): handle invalid repository names gracefully
docs(readme): update installation instructions
```

## Testing

### Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── test_backup_manager.py
│   ├── test_github_client.py
│   └── test_dropbox_client.py
├── integration/            # Integration tests
│   └── test_full_backup.py
└── fixtures/              # Test data
    └── sample_repos.json
```

### Writing Tests

1. **Unit Tests**: Test individual functions/methods
2. **Integration Tests**: Test complete workflows
3. **Mock External APIs**: Don't make real API calls in tests
4. **Test Edge Cases**: Error conditions, empty responses, etc.

Example test:

```python
import pytest
from unittest.mock import Mock, patch
from github_backup.github_client import GitHubClient

def test_get_user_repositories_success():
    client = GitHubClient("fake-token")
    
    with patch.object(client.session, 'get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'name': 'test-repo',
                'full_name': 'user/test-repo',
                'clone_url': 'https://github.com/user/test-repo.git',
                'default_branch': 'main',
                'private': False,
                'size': 1024,
                'updated_at': '2023-01-01T00:00:00Z'
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        repos = client.get_user_repositories()
        
        assert len(repos) == 1
        assert repos[0].name == 'test-repo'
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/github_backup --cov-report=html

# Run specific test file
pytest tests/unit/test_github_client.py

# Run specific test
pytest tests/unit/test_github_client.py::test_get_user_repositories_success
```

## Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Follow Google docstring format
- Include parameter types and return types
- Provide usage examples for complex functions

Example:

```python
def backup_repository(self, repo: Repository) -> bool:
    """Backup a single repository.
    
    Args:
        repo: Repository object to backup.
        
    Returns:
        True if backup successful, False otherwise.
        
    Example:
        >>> backup_manager = BackupManager()
        >>> repo = Repository(...)
        >>> success = backup_manager.backup_repository(repo)
    """
```

### User Documentation

- Update README.md for user-facing changes
- Update docs/ files for detailed documentation
- Include code examples and use cases
- Keep documentation up-to-date with code changes

## Pull Request Process

### Before Submitting

1. **Create an issue** (for non-trivial changes)
2. **Write tests** for your changes
3. **Update documentation** if needed
4. **Run code quality checks**
5. **Test your changes** thoroughly

### PR Description

Include:
- Clear description of changes
- Link to related issue(s)
- Test instructions
- Breaking changes (if any)
- Screenshots (if applicable)

### Review Process

1. Automated checks must pass
2. At least one maintainer review required
3. Address review feedback
4. Maintainer will merge when ready

## Architecture Guidelines

### Project Structure

Follow the established src-layout:
- `src/github_backup/`: Main package code
- `scripts/`: Utility scripts
- `tests/`: Test code
- `docs/`: Documentation

### Design Principles

1. **Single Responsibility**: Each class/function has one purpose
2. **Dependency Injection**: Pass dependencies as parameters
3. **Error Handling**: Graceful error handling with logging
4. **Testability**: Write testable code with minimal dependencies
5. **Type Safety**: Use type hints throughout

### Adding New Features

1. **Plan the API**: Design the public interface first
2. **Write tests**: Test-driven development preferred
3. **Implement incrementally**: Small, focused commits
4. **Document thoroughly**: Code and user documentation
5. **Consider backwards compatibility**: Avoid breaking changes

## Release Process

### Version Numbering

We use Semantic Versioning (semver):
- Major: Breaking changes
- Minor: New features (backwards compatible)
- Patch: Bug fixes

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create release branch
5. Create pull request
6. Tag release after merge
7. Update documentation

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: Tag maintainers in PRs for review

## Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- GitHub contributors page

Thank you for contributing! 🎉
