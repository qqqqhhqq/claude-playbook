#!/usr/bin/env python3
"""
GitHub Repository Structure Fetcher

获取 GitHub 仓库的目录树结构

Usage:
    python github_get_repo_structure.py <repo> [path] [ref] [token]

Args:
    repo: 仓库标识，格式 "owner/repo"
    path: 目录路径，默认为 "/"
    ref: 分支/tag/commit SHA，默认为默认分支
    token: GitHub Personal Access Token (可选)

Example:
    python github_get_repo_structure.py vitejs/vite
    python github_get_repo_structure.py vitejs/vite /src/core main
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List


def get_repo_structure(repo: str, path: str = "", ref: str = None, token: str = None) -> Dict[str, Any]:
    """
    获取 GitHub 仓库的目录结构

    Args:
        repo: 仓库标识 (owner/repo)
        path: 目录路径，空字符串表示根目录
        ref: 分支/tag/commit SHA
        token: GitHub PAT (可选)

    Returns:
        包含目录结构的字典
    """
    # 验证 repo 格式
    if '/' not in repo:
        raise ValueError(f"Invalid repo format: {repo}. Expected 'owner/repo'")

    # 规范化路径
    if path == "/":
        path = ""

    # 构建 API URL
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    if path:
        url = f"https://api.github.com/repos/{repo}/contents/{path}"

    # 添加查询参数
    query_params = []
    if ref:
        query_params.append(f"ref={ref}")

    if query_params:
        url += "?" + "&".join(query_params)

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

            # 处理响应
            if isinstance(data, dict) and data.get("type") == "file":
                # 单个文件
                return {
                    "type": "file",
                    "name": data.get("name"),
                    "path": data.get("path"),
                    "size": data.get("size"),
                    "sha": data.get("sha")
                }

            elif isinstance(data, list):
                # 目录内容
                entries = []
                for item in data:
                    entry = {
                        "name": item.get("name"),
                        "type": item.get("type"),  # "file" or "dir"
                        "path": item.get("path"),
                        "size": item.get("size", 0)
                    }
                    entries.append(entry)

                return {
                    "type": "dir",
                    "path": path or "/",
                    "entries": entries,
                    "total_count": len(entries)
                }

            else:
                raise Exception(f"Unexpected response format: {type(data)}")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            error_msg = f"Path not found: {repo}/{path or '/'}"
        elif e.code == 403:
            error_msg = f"API rate limit exceeded or access forbidden"
        else:
            error_msg = f"HTTP Error {e.code}: {e.reason}"
        raise Exception(error_msg) from e
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e.reason}") from e


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python github_get_repo_structure.py <repo> [path] [ref] [token]", file=sys.stderr)
        print("Example: python github_get_repo_structure.py vitejs/vite", file=sys.stderr)
        print("Example: python github_get_repo_structure.py vitejs/vite /src/core main", file=sys.stderr)
        sys.exit(1)

    repo = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else ""
    ref = sys.argv[3] if len(sys.argv) > 3 else None
    token = sys.argv[4] if len(sys.argv) > 4 else None

    try:
        result = get_repo_structure(repo, path, ref, token)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
