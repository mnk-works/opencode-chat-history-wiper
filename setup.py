"""Setup configuration for OpenCode Chat History Wiper."""

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="opencode-chat-history-wiper",
    version="2.0.0",
    description="Safely clears OpenCode chat history and session logs while preserving credentials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="OpenCode Team",
    author_email="maintainer@example.com",
    url="https://github.com/mnk-works/opencode-chat-history-wiper",
    packages=find_packages(),
    py_modules=["opencode_chat_history_wiper"],
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
    keywords="opencode chat history wipe sessions credentials backup",
    project_urls={
        "Bug Reports": "https://github.com/mnk-works/opencode-chat-history-wiper/issues",
        "Source": "https://github.com/mnk-works/opencode-chat-history-wiper",
        "Documentation": "https://github.com/mnk-works/opencode-chat-history-wiper#readme",
    },
)