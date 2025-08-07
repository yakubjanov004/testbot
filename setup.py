#!/usr/bin/env python3
"""
Setup script for BugBot

This script installs the bugbot command globally.
"""

from setuptools import setup, find_packages

setup(
    name="bugbot",
    version="1.0.0",
    description="Alfa Connect Bot Runner",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    py_modules=["bugbot"],
    entry_points={
        "console_scripts": [
            "bugbot=bugbot:main",
        ],
    },
    install_requires=[
        "aiogram>=3.0.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)