#!/usr/bin/env python3
"""
GitHub File Content Reader

读取 GitHub 仓库中单个文件的完整内容

Usage:
    python github_read_file.py <repo> <path> [ref] [max_size] [token]

Args:
    repo: 仓库标识，格式 "owner/repo"
    path: 文件路径
    ref: 分支/tag/commit SHA (可选)
    max_size: 最大读取字节数，默认 100KB (可选)
    token: GitHub Personal Access Token (可选)

Example:
    python github_read_file.py vitejs/vite README.md
    python github_read_file.py vitejs/vite package.json main
    python github_read_file.py vuejs/vue-router src/router.ts main 50000
"""

import sys
import json
import urllib.request
import urllib.error
import base64
from typing import Dict, Any


def read_file(repo: str, path: str, ref: str = None, max_size: int = 102400, token: str = None) -> Dict[str, Any]:
    """
    读取 GitHub 仓库中的文件内容

    Args:
        repo: 仓库标识 (owner/repo)
        path: 文件路径
        ref: 分支/tag/commit SHA
        max_size: 最大读取字节数，超过则截断
        token: GitHub PAT (可选)

    Returns:
        包含文件内容和元数据的字典
    """
    # 验证输入
    if '/' not in repo:
        raise ValueError(f"Invalid repo format: {repo}. Expected 'owner/repo'")

    if not path:
        raise ValueError("File path is required")

    # 构建 API URL
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    # 添加查询参数
    if ref:
        url += f"?ref={ref}"

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

            # 检查是否为文件
            if data.get("type") != "file":
                raise Exception(f"Path is not a file: {path} (type: {data.get('type')})")

            # 解码 base64 内容
            content_base64 = data.get("content")
            content = base64.b64decode(content_base64).decode('utf-8', errors='replace')

            file_size = len(content.encode('utf-8'))
            truncated = False

            # 检查文件大小并截断
            if file_size > max_size:
                # 按字符截断，保留约 max_size 字节
                content = content[:max_size]
                truncated = True

            return {
                "path": data.get("path"),
                "name": data.get("name"),
                "content": content,
                "size": file_size,
                "sha": data.get("sha"),
                "encoding": "utf-8",
                "truncated": truncated,
                "max_size": max_size if truncated else None
            }

    except urllib.error.HTTPError as e:
        if e.code == 404:
            error_msg = f"File not found: {repo}/{path}"
        elif e.code == 403:
            error_msg = f"API rate limit exceeded or access forbidden"
        else:
            error_msg = f"HTTP Error {e.code}: {e.reason}"
        raise Exception(error_msg) from e
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e.reason}") from e


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("Usage: python github_read_file.py <repo> <path> [ref] [max_size] [token]", file=sys.stderr)
        print("Example: python github_read_file.py vitejs/vite README.md", file=sys.stderr)
        print("Example: python github_read_file.py vitejs/vite package.json main", file=sys.stderr)
        sys.exit(1)

    repo = sys.argv[1]
    path = sys.argv[2]
    ref = sys.argv[3] if len(sys.argv) > 3 else None
    max_size = int(sys.argv[4]) if len(sys.argv) > 4 else 102400  # 100KB 默认
    token = sys.argv[5] if len(sys.argv) > 5 else None

    try:
        result = read_file(repo, path, ref, max_size, token)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
