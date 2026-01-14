#!/usr/bin/env python3
"""
GitHub Repository Info Fetcher

获取 GitHub 仓库的基本信息（描述、语言、星标数等）

Usage:
    python github_get_repo_info.py <repo> [token]

Args:
    repo: 仓库标识，格式 "owner/repo" (例如: "vitejs/vite")
    token: GitHub Personal Access Token (可选，用于提高 API 限流)

Example:
    python github_get_repo_info.py vitejs/vite
    python github_get_repo_info.py vuejs/vue-router ghp_xxxxx
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any


def get_repo_info(repo: str, token: str = None) -> Dict[str, Any]:
    """
    获取 GitHub 仓库信息

    Args:
        repo: 仓库标识 (owner/repo)
        token: GitHub PAT (可选)

    Returns:
        包含仓库信息的字典

    Raises:
        urllib.error.HTTPError: API 请求失败
    """
    # 验证 repo 格式
    if '/' not in repo:
        raise ValueError(f"Invalid repo format: {repo}. Expected 'owner/repo'")

    # 构建请求 URL
    url = f"https://api.github.com/repos/{repo}"

    # 设置请求头
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "github-code-analyzer"
    }

    if token:
        headers["Authorization"] = f"token {token}"

    # 创建请求
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

            # 提取关键信息
            result = {
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "description": data.get("description"),
                "language": data.get("language"),
                "languages_url": data.get("languages_url"),
                "default_branch": data.get("default_branch"),
                "stargazers_count": data.get("stargazers_count"),
                "forks_count": data.get("forks_count"),
                "open_issues_count": data.get("open_issues_count"),
                "homepage": data.get("homepage"),
                "topics": data.get("topics", []),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "size": data.get("size"),
                "license": data.get("license", {}).get("name") if data.get("license") else None
            }

            return result

    except urllib.error.HTTPError as e:
        if e.code == 404:
            error_msg = f"Repository not found: {repo}"
        elif e.code == 403:
            error_msg = f"API rate limit exceeded. Try again later or provide a token."
        else:
            error_msg = f"HTTP Error {e.code}: {e.reason}"
        raise Exception(error_msg) from e
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e.reason}") from e


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python github_get_repo_info.py <repo> [token]", file=sys.stderr)
        print("Example: python github_get_repo_info.py vitejs/vite", file=sys.stderr)
        sys.exit(1)

    repo = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = get_repo_info(repo, token)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
