"""
Setup script for the Command Capture library.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = ""
readme_path = this_directory / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text()

setup(
    name="cmdcapture",
    version="1.0.0",
    author="Command Capture Library",
    author_email="wertex3233@gmail.com",
    description="A Python library for capturing output from terminal commands with advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jejis06/CommandCapture",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - using only standard library
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ]
    },
    entry_points={
        "console_scripts": [
            "cmdcapture=cmdcapture.cli:main",
        ],
    },
    keywords="command capture subprocess terminal shell output",
    project_urls={
        "Bug Reports": "https://github.com/Jejis06/CommandCapture/issues",
        "Source": "https://github.com/Jejis06/CommandCapture",
    },
) 