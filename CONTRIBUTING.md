# Contributing to RCS Simulations

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the RCS simulation repository.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the [Issues](https://github.com/lpurdy01/rcs/issues) section
2. If not, create a new issue with a clear title and description
3. Include relevant details:
   - Your operating system and version
   - Python version
   - openEMS version
   - Steps to reproduce the issue
   - Expected behavior vs. actual behavior

### Submitting Changes

1. **Fork the Repository**
   - Create a fork of this repository to your GitHub account

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
   or
   ```bash
   git checkout -b fix/your-bug-fix
   ```

3. **Make Your Changes**
   - Keep changes focused and atomic
   - Follow the existing code style
   - Test your changes thoroughly

4. **Commit Your Changes**
   - Write clear, concise commit messages
   - Reference any related issues
   ```bash
   git commit -m "Add feature: description of feature"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Provide a clear description of your changes

## Code Guidelines

### Python Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions and classes

### Example Simulations

When adding new example simulations:

- Include a clear docstring at the top describing the simulation
- Specify tested Python and openEMS versions
- Use descriptive variable names
- Add comments explaining key simulation parameters
- Save results to temporary directories by default

Example template:
```python
# -*- coding: utf-8 -*-
"""
Description of your simulation

Tested with
 - python 3.10
 - openEMS v0.0.35+

Author information
"""

### Import Libraries
import os, tempfile
from pylab import *

# Your simulation code here
```

### Documentation

When updating documentation:

- Use clear, concise language
- Include code examples where appropriate
- Keep formatting consistent with existing docs
- Update the README.md if adding new features

## Types of Contributions

We welcome various types of contributions:

- **New simulation examples**: Additional antenna designs, RCS targets, or other EM structures
- **Bug fixes**: Corrections to existing code or documentation
- **Performance improvements**: Optimizations to simulation setups
- **Documentation**: Improvements to README, comments, or tutorials
- **Setup scripts**: Additional installation or configuration scripts
- **Test targets**: New STL models or geometry definitions

## Testing

Before submitting a pull request:

1. Test that your simulation runs successfully
2. Verify that results are reasonable
3. Check that existing examples still work
4. Ensure documentation is accurate

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the "question" label
- Contact the repository maintainers

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

Thank you for contributing to the RCS Simulations project!
