#!/usr/bin/env python3
"""
SHADOWSCAN PRO - Setup Configuration
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="shadowscan-pro",
    version="1.0.0",
    author="ROHAIB TECHNICAL",
    author_email="rohaib@technical.com",
    description="Advanced Offensive Security & Auto-Exploitation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohaib11/shadowscan-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: Proprietary",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "shadowscan=shadowscan.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "shadowscan": [
            "config/*.yaml",
            "config/*.txt",
            "data/**/*",
        ],
    },
    zip_safe=False,
)