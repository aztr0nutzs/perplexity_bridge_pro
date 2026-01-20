# Contributing to Perplexity Bridge Pro

Thank you for your interest in contributing to Perplexity Bridge Pro! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Workflow](#development-workflow)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/perplexity_bridge_pro.git
   cd perplexity_bridge_pro
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/aztr0nutzs/perplexity_bridge_pro.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Node.js 14+ (for VSCode extension development)

### Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env and add your API keys
   ```

4. **Install pre-commit hooks** (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Running the Application

```bash
python start.py
```

The server will start on `http://127.0.0.1:7860`

## Code Style Guidelines

We follow Python best practices and PEP 8 style guidelines with some modifications:

### Python Code Style

- **Line length**: Maximum 120 characters (configured in Black)
- **Imports**: Use absolute imports, group them logically (standard library, third-party, local)
- **Type hints**: All functions should have type hints for parameters and return values
- **Docstrings**: Use docstrings for all public functions, classes, and modules
- **Naming conventions**:
  - Classes: `PascalCase`
  - Functions/methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private members: `_leading_underscore`

### Formatting Tools

We use automated tools to maintain consistent code style:

- **Black**: Code formatter (line length: 120)
- **Flake8**: Linting
- **MyPy**: Type checking
- **isort**: Import sorting

Run all formatters:
```bash
black .
isort .
flake8 .
mypy .
```

### Pre-commit Hooks

Pre-commit hooks automatically run formatters and linters before each commit:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON validation
- Large file detection
- Private key detection
- Black formatting
- Flake8 linting
- MyPy type checking

## Testing Requirements

All contributions must include appropriate tests:

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=term --cov-report=html

# Run specific test file
pytest tests/test_app.py

# Run specific test
pytest tests/test_app.py::test_health_endpoint
```

### Test Guidelines

- Write tests for all new features and bug fixes
- Maintain or improve code coverage (minimum 80% required)
- Use descriptive test names: `test_<what>_<condition>_<expected>`
- Use pytest fixtures for common setup
- Mock external API calls using `unittest.mock`
- Test both success and error cases
- Test edge cases and boundary conditions

### Test Structure

```python
def test_feature_name_condition_expected():
    """Test description explaining what is being tested."""
    # Arrange: Set up test data and conditions
    
    # Act: Execute the code being tested
    
    # Assert: Verify expected outcomes
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Write/update tests** for your changes

4. **Run the test suite**:
   ```bash
   pytest --cov=. --cov-report=term
   ```

5. **Run linters and formatters**:
   ```bash
   black .
   flake8 .
   mypy .
   ```

6. **Update documentation** if necessary (README, docstrings, etc.)

7. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```
   
   Use conventional commit messages:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes (formatting, etc.)
   - `refactor:` Code refactoring
   - `test:` Adding or updating tests
   - `chore:` Maintenance tasks

### Submitting the PR

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Link to any related issues
   - Screenshots for UI changes
   - Test results and coverage report

3. **Wait for review**:
   - Address any feedback from reviewers
   - Make requested changes in new commits
   - Push updates to the same branch

4. **After approval**:
   - Maintainers will merge your PR
   - Your changes will be included in the next release

### PR Checklist

- [ ] Code follows the style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Code coverage maintained or improved (≥80%)
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow conventional format
- [ ] No merge conflicts with main branch
- [ ] PR description clearly explains the changes

## Issue Reporting

### Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Exact steps to reproduce the behavior
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**:
   - OS (Windows/macOS/Linux)
   - Python version
   - Package versions
6. **Logs**: Relevant error messages or logs
7. **Screenshots**: If applicable

### Feature Requests

When requesting features, include:

1. **Description**: Clear description of the proposed feature
2. **Use case**: Why this feature would be useful
3. **Proposed implementation**: How you think it should work (optional)
4. **Alternatives**: Alternative solutions you've considered
5. **Additional context**: Any other relevant information

### Security Issues

**Do not report security vulnerabilities through public GitHub issues.**

Please see [SECURITY.md](SECURITY.md) for instructions on reporting security issues.

## Development Workflow

### Syncing with Upstream

Keep your fork updated with the main repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Working on Issues

1. Check existing issues or create a new one
2. Comment on the issue to indicate you're working on it
3. Create a feature branch from main
4. Implement your changes
5. Submit a pull request referencing the issue

### Code Review Process

All submissions require review before merging:

1. Automated checks must pass (CI/CD pipeline)
2. At least one maintainer approval required
3. Address all review comments
4. Keep the PR scope focused and manageable

## Additional Resources

- [README.md](README.md) - Project overview and usage
- [SECURITY.md](SECURITY.md) - Security policy
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Detailed testing guide
- [INSTALL.md](INSTALL.md) - Installation instructions

## Questions?

If you have questions or need help:

1. Check existing documentation
2. Search existing issues
3. Create a new issue with the `question` label
4. Join community discussions

Thank you for contributing to Perplexity Bridge Pro! 🚀
