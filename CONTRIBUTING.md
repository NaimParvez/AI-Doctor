# Contributing to AI Doctor Jhatka

First off, thank you for considering contributing to AI Doctor Jhatka! It's people like you that make this project possible and help improve healthcare accessibility through AI.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Guidelines](#development-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting Guidelines](#issue-reporting-guidelines)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)
- Ollama installed locally
- Basic understanding of Flask, SQLAlchemy, and web development

### Setting Up Development Environment

1. **Fork and Clone**

   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Doctor-Jhatka.git
   cd AI-Doctor-Jhatka
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

4. **Set Up Environment Variables**

   ```bash
   cp .env.example .env  # If available
   # Edit .env with your configuration
   ```

5. **Initialize Database**

   ```bash
   flask db upgrade
   ```

6. **Run Tests**
   ```bash
   pytest
   ```

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When you are creating a bug report, please include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**

- OS: [e.g. Windows 11, macOS Big Sur, Ubuntu 20.04]
- Python Version: [e.g. 3.10.0]
- Browser: [e.g. Chrome 120.0, Firefox 119.0]
- Project Version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Clear title and description** of the enhancement
- **Detailed explanation** of the proposed functionality
- **Use cases** that demonstrate the need for this enhancement
- **Mockups or examples** if applicable
- **Consider the scope** - is this a core feature or plugin material?

### 🔧 Code Contributions

#### Areas We Need Help With

**High Priority:**

- [ ] Improve AI model accuracy and medical knowledge
- [ ] Enhance security features and authentication
- [ ] Add comprehensive test coverage
- [ ] Performance optimization
- [ ] Mobile responsiveness improvements

**Medium Priority:**

- [ ] Internationalization (i18n) support
- [ ] Advanced medical features (appointment scheduling, medication reminders)
- [ ] Integration with external health APIs
- [ ] Analytics and reporting features
- [ ] Email notifications

**Beginner Friendly:**

- [ ] UI/UX improvements
- [ ] Documentation updates
- [ ] Bug fixes
- [ ] Code refactoring
- [ ] Adding more test cases

## Development Guidelines

### 🎨 Code Style

We follow PEP 8 for Python code style. Please ensure your code adheres to these guidelines:

```python
# Good example
def process_medical_query(query: str, user_context: Dict[str, Any]) -> str:
    """
    Process a medical query using the AI model.

    Args:
        query: The user's medical question
        user_context: User information for personalized responses

    Returns:
        AI-generated medical response

    Raises:
        ModelError: If the AI model fails to process the query
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")

    # Implementation here
    return response
```

**Key Points:**

- Use type hints for function parameters and return values
- Write clear docstrings for all functions and classes
- Use meaningful variable names
- Keep functions small and focused (< 50 lines ideally)
- Add comments for complex logic

### 🧪 Testing

All code contributions should include appropriate tests:

```python
# Example test case
def test_user_registration_with_valid_data(client):
    """Test user registration with valid data."""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepass123',
        'date_of_birth': '1990-01-01',
        'gender': 'male'
    })
    assert response.status_code == 302
    assert User.query.filter_by(username='testuser').first() is not None
```

**Testing Requirements:**

- Write unit tests for new functions
- Write integration tests for new endpoints
- Ensure all tests pass before submitting
- Aim for >80% code coverage
- Test both positive and negative scenarios

### 🗄️ Database Changes

When making database schema changes:

1. **Create Migration**

   ```bash
   flask db migrate -m "Descriptive migration message"
   ```

2. **Review Migration File**

   - Check the generated migration for accuracy
   - Ensure it's reversible (has both upgrade and downgrade)

3. **Test Migration**
   ```bash
   flask db upgrade
   flask db downgrade  # Test rollback
   flask db upgrade    # Re-apply
   ```

### 🔒 Security Considerations

- Never commit sensitive information (API keys, passwords, etc.)
- Use environment variables for configuration
- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Follow OWASP security guidelines

## Pull Request Process

### 1. Before Creating a PR

- [ ] Ensure all tests pass locally
- [ ] Run linting and code formatting
- [ ] Update documentation if needed
- [ ] Add/update tests for new functionality
- [ ] Check that your changes don't break existing functionality

### 2. Creating the PR

**PR Title Format:**

```
type(scope): brief description

Examples:
feat(auth): add two-factor authentication
fix(chat): resolve message ordering issue
docs(readme): update installation instructions
test(models): add user model validation tests
```

**PR Description Template:**

```markdown
## Description

Brief description of the changes made.

## Related Issue

Fixes #123

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?

Please describe the tests that you ran to verify your changes.

## Screenshots (if applicable)

Add screenshots for UI changes.

## Checklist

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### 3. Review Process

- Maintainers will review your PR within 48-72 hours
- Address any feedback or requested changes
- Keep discussions respectful and constructive
- Make necessary updates and push to your branch

### 4. Merging

- PRs require at least one approving review from a maintainer
- All CI checks must pass
- No merge conflicts
- Branch will be merged using "Squash and merge" strategy

## Issue Reporting Guidelines

### 🐛 Bug Reports

**Before Reporting:**

- Search existing issues to avoid duplicates
- Try to reproduce the issue with the latest version
- Gather relevant information about your environment

**Required Information:**

- Clear, descriptive title
- Step-by-step reproduction instructions
- Expected vs actual behavior
- Environment details (OS, Python version, browser)
- Error messages or logs
- Screenshots if applicable

### 💡 Feature Requests

**Before Requesting:**

- Check if the feature already exists
- Search existing feature requests
- Consider if this belongs in core or as a plugin

**Required Information:**

- Clear use case description
- Detailed feature specification
- Potential implementation approach
- Consider backwards compatibility

## Community

### 🗨️ Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community discussion
- **Discord**: Real-time chat and support (if available)
- **Email**: Direct contact with maintainers for sensitive issues

### 🎯 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and experiences
- Give constructive feedback
- Follow our Code of Conduct

### 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- CHANGELOG.md for significant contributions
- GitHub releases notes
- Special mentions in project updates

## Questions?

Don't hesitate to ask questions! We're here to help:

- Create a [GitHub Discussion](https://github.com/NaimParvez/AI-Doctor/discussions)
- Open an issue with the "question" label
- Contact maintainers directly for sensitive matters

Thank you for contributing to AI Doctor Jhatka! 🙏
