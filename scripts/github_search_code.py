#!/usr/bin/env python3
"""
GitHub Code Searcher

在 GitHub 仓库中搜索匹配关键词的代码

Usage:
    python github_search_code.py <repo> <query> [ref] [language] [token]

Args:
    repo: 仓库标识，格式 "owner/repo"
    query: 搜索关键词
    ref: 限定分支 (可选)
    language: 语言过滤，如 "Python", "TypeScript" (可选)
    token: GitHub Personal Access Token (可选)

Example:
    python github_search_code.py vitejs/vite "plugin system"
    python github_search_code.py vuejs/vue-router "router" main TypeScript
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List
from urllib.parse import quote


def search_code(repo: str, query: str, ref: str = None, language: str = None, token: str = None) -> Dict[str, Any]:
    """
    在 GitHub 仓库中搜索代码

    Args:
        repo: 仓库标识 (owner/repo)
        query: 搜索关键词
        ref: 限定分支
        language: 语言过滤
        token: GitHub PAT (可选)

    Returns:
        包含搜索结果的字典
    """
    # 验证输入
    if '/' not in repo:
        raise ValueError(f"Invalid repo format: {repo}. Expected 'owner/repo'")

    if not query:
        raise ValueError("Search query is required")

    # 构建搜索查询
    # 格式: query+repo:owner/repo+language:TypeScript+ref:main
    query_parts = [quote(query)]
    query_parts.append(f"repo:{repo}")

    if language:
        query_parts.append(f"language:{language}")

    if ref:
        query_parts.append(f"ref:{ref}")

    search_query = "+".join(query_parts)

    # 构建 API URL
    url = f"https://api.github.com/search/code?q={search_query}&per_page=10"

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
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

            # 处理搜索结果
            total_count = data.get("total_count", 0)
            items = data.get("items", [])

            results = []
            for item in items:
                # 提取文本匹配信息（如果 API 返回）
                text_matches = item.get("text_matches", [])

                matches = []
                if text_matches:
                    for match in text_matches:
                        matches.append({
                            "line_number": match.get("matches", [{}])[0].get("start", 0),
                            "fragment": match.get("fragment", "")
                        })

                result = {
                    "name": item.get("name"),
                    "path": item.get("path"),
                    "sha": item.get("sha"),
                    "html_url": item.get("html_url"),
                    "score": item.get("score"),
                    "matches": matches[:3] if matches else []  # 只保留前3个匹配
                }
                results.append(result)

            return {
                "total_count": total_count,
                "count": len(results),
                "query": query,
                "results": results
            }

    except urllib.error.HTTPError as e:
        if e.code == 403:
            error_msg = f"API rate limit exceeded or access forbidden"
        elif e.code == 422:
            error_msg = f"Search validation failed. Check your query parameters."
        else:
            error_msg = f"HTTP Error {e.code}: {e.reason}"
        raise Exception(error_msg) from e
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e.reason}") from e


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("Usage: python github_search_code.py <repo> <query> [ref] [language] [token]", file=sys.stderr)
        print("Example: python github_search_code.py vitejs/vite 'plugin'", file=sys.stderr)
        print("Example: python github_search_code.py vuejs/vue-router 'router' main TypeScript", file=sys.stderr)
        sys.exit(1)

    repo = sys.argv[1]
    query = sys.argv[2]
    ref = sys.argv[3] if len(sys.argv) > 3 else None
    language = sys.argv[4] if len(sys.argv) > 4 else None
    token = sys.argv[5] if len(sys.argv) > 5 else None

    try:
        result = search_code(repo, query, ref, language, token)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
