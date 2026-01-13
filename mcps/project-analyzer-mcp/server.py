#!/usr/bin/env python3
"""
Project Analyzer MCP Server

提供项目分析功能的 MCP 服务器，支持：
- 分析目录结构
- 统计代码行数
- 列出项目依赖
"""

import ast
import json
import os
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 服务器配置
server = Server("project-analyzer-mcp")

# 支持的编程语言文件扩展
CODE_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React JSX',
    '.tsx': 'React TSX',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'C/C++ Header',
    '.cs': 'C#',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.sh': 'Shell',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.json': 'JSON',
    '.xml': 'XML',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.less': 'LESS',
    '.md': 'Markdown',
}

# 依赖文件映射
DEPENDENCY_FILES = {
    'requirements.txt': 'pip',
    'package.json': 'npm',
    'package-lock.json': 'npm',
    'yarn.lock': 'yarn',
    'pnpm-lock.yaml': 'pnpm',
    'pom.xml': 'Maven',
    'build.gradle': 'Gradle',
    'Cargo.toml': 'Cargo',
    'go.mod': 'Go Modules',
    'composer.json': 'Composer',
    'Gemfile': 'Bundler',
    'Podfile': 'CocoaPods',
}


def analyze_directory(path: str, max_depth: int = 3) -> dict:
    """
    分析目录结构

    Args:
        path: 目录路径
        max_depth: 最大递归深度

    Returns:
        包含目录结构的字典
    """
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        return {'error': f'路径不存在或不是目录: {path}'}

    def build_tree(current_path: Path, current_depth: int) -> dict:
        if current_depth > max_depth:
            return {'name': current_path.name, 'type': 'dir', 'truncated': True}

        try:
            entries = []
            for item in sorted(current_path.iterdir()):
                # 跳过隐藏文件和常见忽略目录
                if item.name.startswith('.'):
                    continue
                if item.is_dir() and item.name in {'node_modules', '__pycache__', 'venv', '.venv', 'target', 'build', 'dist'}:
                    continue

                if item.is_dir():
                    entries.append(build_tree(item, current_depth + 1))
                else:
                    ext = item.suffix.lower()
                    lang = CODE_EXTENSIONS.get(ext, 'Unknown')
                    entries.append({
                        'name': item.name,
                        'type': 'file',
                        'language': lang,
                        'size': item.stat().st_size,
                    })
            return {
                'name': current_path.name,
                'type': 'dir',
                'path': str(current_path),
                'entries': entries,
            }
        except PermissionError:
            return {'name': current_path.name, 'type': 'dir', 'error': 'Permission denied'}

    return build_tree(root, 0)


def count_lines(path: str, by_language: bool = True) -> dict:
    """
    统计代码行数

    Args:
        path: 目录路径
        by_language: 是否按语言分类统计

    Returns:
        代码行数统计结果
    """
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        return {'error': f'路径不存在或不是目录: {path}'}

    stats = {}
    total_lines = 0
    total_files = 0

    for file_path in root.rglob('*'):
        if file_path.is_file() and not file_path.name.startswith('.'):
            ext = file_path.suffix.lower()
            if ext in CODE_EXTENSIONS:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = sum(1 for _ in f)
                        lang = CODE_EXTENSIONS[ext]
                        if by_language:
                            if lang not in stats:
                                stats[lang] = {'files': 0, 'lines': 0}
                            stats[lang]['files'] += 1
                            stats[lang]['lines'] += lines
                        else:
                            total_files += 1
                            total_lines += lines
                except (PermissionError, UnicodeDecodeError):
                    pass

    if by_language:
        return {
            'by_language': stats,
            'total_files': sum(s['files'] for s in stats.values()),
            'total_lines': sum(s['lines'] for s in stats.values()),
        }
    return {'files': total_files, 'lines': total_lines}


def list_dependencies(path: str) -> dict:
    """
    列出项目依赖

    Args:
        path: 目录路径

    Returns:
        项目依赖信息
    """
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        return {'error': f'路径不存在或不是目录: {path}'}

    dependencies = {}

    for dep_file, manager in DEPENDENCY_FILES.items():
        file_path = root / dep_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                deps = []
                if dep_file == 'requirements.txt':
                    deps = [line.strip().split('==')[0].split('>=')[0].split('<=')[0]
                           for line in content.split('\n')
                           if line.strip() and not line.startswith('#')]
                elif dep_file in ['package.json', 'composer.json', 'Cargo.toml', 'go.mod']:
                    try:
                        data = json.loads(content) if dep_file.endswith('.json') else {}
                        if dep_file == 'package.json':
                            deps = list(data.get('dependencies', {}).keys())
                            deps += list(data.get('devDependencies', {}).keys())
                    except json.JSONDecodeError:
                        pass
                elif dep_file == 'pom.xml':
                    # 简化的 XML 解析
                    import re
                    deps = re.findall(r'<artifactId>([^<]+)</artifactId>', content)

                if deps:
                    dependencies[manager] = {
                        'file': dep_file,
                        'count': len(deps),
                        'dependencies': deps[:20],  # 限制返回数量
                        'truncated': len(deps) > 20,
                    }
            except (PermissionError, UnicodeDecodeError):
                pass

    return {
        'dependency_managers': list(dependencies.keys()),
        'dependencies': dependencies,
    }


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="analyze_structure",
            description="分析项目的目录结构，返回文件树。支持设置最大递归深度。",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "项目根目录路径（默认为当前工作目录）",
                    },
                    "max_depth": {
                        "type": "number",
                        "description": "最大递归深度（默认 3）",
                        "default": 3,
                        "minimum": 1,
                        "maximum": 10,
                    },
                },
            },
        ),
        Tool(
            name="count_lines",
            description="统计项目代码行数，支持按编程语言分类。",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "项目根目录路径（默认为当前工作目录）",
                    },
                    "by_language": {
                        "type": "boolean",
                        "description": "是否按语言分类统计（默认 true）",
                        "default": True,
                    },
                },
            },
        ),
        Tool(
            name="list_dependencies",
            description="列出项目的依赖包和依赖管理器。",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "项目根目录路径（默认为当前工作目录）",
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """处理工具调用"""
    path = arguments.get('path', os.getcwd())

    if name == "analyze_structure":
        max_depth = arguments.get('max_depth', 3)
        result = analyze_directory(path, max_depth)
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]

    elif name == "count_lines":
        by_language = arguments.get('by_language', True)
        result = count_lines(path, by_language)
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]

    elif name == "list_dependencies":
        result = list_dependencies(path)
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """启动服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
