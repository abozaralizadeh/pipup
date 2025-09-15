#!/usr/bin/env python3
"""
Setup script for pipup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="requp",
    version="1.1.1",
    author="Abozar Alizadeh",
    author_email="abozar@example.com",
    description="Update Python package versions in requirements.txt with exact versions from pip freeze",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abozaralizadeh/pipup",
    py_modules=["pipup"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Archiving :: Packaging",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "pipup=pipup:main",
            "requp=pipup:main",
        ],
    },
    keywords="pip requirements version management python packaging",
    project_urls={
        "Bug Reports": "https://github.com/abozaralizadeh/pipup/issues",
        "Source": "https://github.com/abozaralizadeh/pipup",
    },
)
