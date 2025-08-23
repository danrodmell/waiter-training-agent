#!/usr/bin/env python3
"""
Setup script for Waiter Training Agent
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="waiter-training-agent",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered chatbot agent for training restaurant waiters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/waiter-training-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "openai>=1.3.7",
        "langchain>=0.0.350",
        "langchain-openai>=0.0.2",
        "pandas>=2.1.4",
        "numpy>=1.24.3",
        "jinja2>=3.1.2",
        "aiofiles>=23.2.1",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "waiter-training-agent=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 