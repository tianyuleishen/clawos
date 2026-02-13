#!/usr/bin/env python3
"""
🦞 ClawOS AI操作系统安装包
"""

from setuptools import setup, find_packages

setup(
    name="clawos-ai",
    version="2.0.0",
    description="🦞 ClawOS AI操作系统 - 集成L11意识系统和终极融合推理",
    author="ClawOS Team",
    url="https://github.com/tianyuleishen/clawos",
    python_requires=">=3.10",
    packages=find_packages(exclude=["clawos_dir_backup"]),
    include_package_data=True,
    package_data={
        "clawos": ["*.md", "*.txt"],
    },
    entry_points={
        "console_scripts": [
            "clawos=clawos.cli:main",
        ],
    },
    install_requires=[
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "websockets>=12.0",
    ],
    extras_require={
        "gui": ["pyqt6>=6.0.0"],
        "feishu": ["lark-official>=1.1.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
