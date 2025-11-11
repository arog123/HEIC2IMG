# Contributing to HEIC to JPG/PNG Converter

Thank you for your interest in contributing to this project! We welcome contributions from everyone.

## Table of Contents

- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version)
- Error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- A clear description of the feature
- Why this feature would be useful
- Possible implementation approaches
- Any examples from similar applications

### Code Contributions

We welcome pull requests for:

- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Code refactoring
- Test coverage improvements

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/arog123/HEIC2IMG.git
   cd HEIC2IMG
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   or
   ```bash
   git checkout -b fix/issue-description
   ```

## Development Setup

1. **Install Python 3.7+** (if not already installed)

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the application:**
   ```bash
   python3 app.py
   ```

## Submitting Changes

1. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```
   
   Write clear, concise commit messages. Use present tense ("Add feature" not "Added feature").

2. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request:**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Provide a clear title and description
   - Reference any related issues (e.g., "Fixes #123")

### Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Update documentation if needed
- Test your changes thoroughly
- Ensure code follows the project's coding standards
- Respond to feedback and requested changes promptly

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Code Organization

- Keep functions focused and single-purpose
- Add docstrings to classes and complex functions
- Use comments to explain "why", not "what"
- Handle exceptions appropriately with try/except blocks

### Example Style

```python
def convert_image(input_path, output_format):
    """
    Convert HEIC image to specified format.
    
    Args:
        input_path (str): Path to the HEIC file
        output_format (str): Output format ('JPG' or 'PNG')
    
    Returns:
        str: Path to the converted file
    
    Raises:
        ValueError: If format is not supported
        FileNotFoundError: If input file doesn't exist
    """
    # Implementation here
    pass
```

## Feature Ideas

If you're looking for ways to contribute, here are some ideas:

- Batch conversion support (multiple files at once)
- Progress bar for conversion
- Quality slider for JPG output
- Resize options during conversion
- Preview of converted image before saving
- Custom output directory selection
- Command-line interface option
- Support for additional input formats (HEIF, AVIF)
- Dark mode UI theme
- Conversion history/log
- Unit tests and automated testing

## Testing

Before submitting a PR, please test:

- Loading files via browse button
- Drag and drop functionality
- Both JPG and PNG conversion
- Error handling (invalid files, missing files)
- UI responsiveness
- Cross-platform compatibility (if possible)

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Check existing issues and discussions
- Review the README.md for project documentation

## Recognition

Contributors will be acknowledged in the project. Thank you for helping improve this tool!

## Makefile Usage

### Setup:

make install - Install dependencies
make install-dev - Install dev dependencies (includes PyInstaller, pytest, etc.)
make venv - Create virtual environment
make dev-setup - Complete dev setup (venv + dependencies)

### Development:

make run - Run the application
make test - Run tests
make test-verbose - Run tests with verbose output
make lint - Check code style
make format - Auto-format code
make check - Run lint + test

### Building:

make build - Interactive build (uses build.py)
make build-quick - Quick build
make build-clean - Clean build (removes old files first)
make verify - Check if executable was built

### Cleanup:

make clean - Remove build artifacts
make clean-all - Remove everything including venv

### Special:

make release - Full release build (clean, test, build, verify)
make info - Show project information
make help - Show all available commands

---

**Happy Contributing!** 🎉