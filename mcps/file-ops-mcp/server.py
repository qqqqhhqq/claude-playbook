#!/usr/bin/env python3
"""
File Operations MCP Server

提供基础文件操作功能的 MCP 服务器，支持：
- 读取文件
- 写入文件
- 搜索文件
"""

import fnmatch
import json
import os
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 服务器配置
server = Server("file-ops-mcp")

# 默认允许访问的根目录（可配置）
ALLOWED_ROOTS = os.environ.get('FILE_OPS_ROOT', os.getcwd()).split(os.pathsep)


def is_path_allowed(path: str) -> bool:
    """
    检查路径是否在允许访问的范围内

    Args:
        path: 要检查的文件路径

    Returns:
        是否允许访问
    """
    try:
        abs_path = Path(path).resolve()
        for root in ALLOWED_ROOTS:
            if abs_path.is_relative_to(Path(root).resolve()):
                return True
        return False
    except (OSError, ValueError):
        return False


def read_file(path: str, encoding: str = 'utf-8') -> dict:
    """
    读取文件内容

    Args:
        path: 文件路径
        encoding: 文件编码

    Returns:
        包含文件内容和元数据的字典
    """
    if not is_path_allowed(path):
        return {'error': f'访问被拒绝: 路径不在允许的范围内: {path}'}

    file_path = Path(path).resolve()

    if not file_path.exists():
        return {'error': f'文件不存在: {path}'}

    if not file_path.is_file():
        return {'error': f'不是文件: {path}'}

    try:
        content = file_path.read_text(encoding=encoding, errors='replace')
        return {
            'path': str(file_path),
            'name': file_path.name,
            'size': file_path.stat().st_size,
            'encoding': encoding,
            'content': content,
            'line_count': len(content.splitlines()),
        }
    except PermissionError:
        return {'error': f'权限不足: {path}'}
    except UnicodeDecodeError:
        return {'error': f'编码错误: 无法用 {encoding} 解码文件'}


def write_file(path: str, content: str, encoding: str = 'utf-8', create_dirs: bool = False) -> dict:
    """
    写入文件内容

    Args:
        path: 文件路径
        content: 文件内容
        encoding: 文件编码
        create_dirs: 是否自动创建目录

    Returns:
        操作结果
    """
    if not is_path_allowed(path):
        return {'error': f'访问被拒绝: 路径不在允许的范围内: {path}'}

    file_path = Path(path).resolve()

    # 检查父目录是否存在
    if create_dirs and not file_path.parent.exists():
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return {'error': f'无法创建目录: {e}'}

    if not file_path.parent.exists():
        return {'error': f'父目录不存在: {file_path.parent}'}

    try:
        file_path.write_text(content, encoding=encoding)
        return {
            'success': True,
            'path': str(file_path),
            'bytes_written': len(content.encode(encoding)),
        }
    except PermissionError:
        return {'error': f'权限不足: {path}'}
    except OSError as e:
        return {'error': f'写入失败: {e}'}


def search_files(
    directory: str,
    pattern: str = '*',
    content_pattern: str = None,
    max_results: int = 100
) -> dict:
    """
    搜索文件

    Args:
        directory: 搜索目录
        pattern: 文件名模式（支持通配符）
        content_pattern: 文件内容模式（可选，在文件中搜索）
        max_results: 最大结果数量

    Returns:
        搜索结果列表
    """
    if not is_path_allowed(directory):
        return {'error': f'访问被拒绝: 路径不在允许的范围内: {directory}'}

    root_path = Path(directory).resolve()

    if not root_path.exists():
        return {'error': f'目录不存在: {directory}'}

    if not root_path.is_dir():
        return {'error': f'不是目录: {directory}'}

    results = []

    try:
        for file_path in root_path.rglob('*'):
            if len(results) >= max_results:
                break

            if not file_path.is_file():
                continue

            # 跳过隐藏文件和常见忽略目录
            if any(part.startswith('.') for part in file_path.parts):
                continue
            if any(part in {'node_modules', '__pycache__', 'venv', '.venv', 'target', 'build', 'dist', '.git'}
                   for part in file_path.parts):
                continue

            # 文件名匹配
            if not fnmatch.fnmatch(file_path.name, pattern):
                continue

            result = {
                'path': str(file_path.relative_to(root_path)),
                'name': file_path.name,
                'size': file_path.stat().st_size,
            }

            # 内容搜索
            if content_pattern:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f, 1):
                            if content_pattern.lower() in line.lower():
                                result['matches'] = result.get('matches', [])
                                if len(result['matches']) < 5:  # 限制每个文件的匹配数
                                    result['matches'].append({
                                        'line': i,
                                        'text': line.strip()[:100],
                                    })
                                break
                        if 'matches' not in result:
                            continue
                except (PermissionError, UnicodeDecodeError):
                    continue

            results.append(result)

        return {
            'directory': str(root_path),
            'pattern': pattern,
            'content_pattern': content_pattern,
            'count': len(results),
            'results': results,
        }

    except PermissionError:
        return {'error': f'权限不足: {directory}'}
    except OSError as e:
        return {'error': f'搜索失败: {e}'}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="read_file",
            description="读取文件内容。支持指定编码方式。需要文件路径在允许的访问范围内。",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "文件路径",
                    },
                    "encoding": {
                        "type": "string",
                        "description": "文件编码（默认 utf-8）",
                        "default": "utf-8",
                    },
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="write_file",
            description="写入文件内容。可选择是否自动创建父目录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "文件路径",
                    },
                    "content": {
                        "type": "string",
                        "description": "文件内容",
                    },
                    "encoding": {
                        "type": "string",
                        "description": "文件编码（默认 utf-8）",
                        "default": "utf-8",
                    },
                    "create_dirs": {
                        "type": "boolean",
                        "description": "自动创建父目录（默认 false）",
                        "default": False,
                    },
                },
                "required": ["path", "content"],
            },
        ),
        Tool(
            name="search_files",
            description="在目录中搜索文件，支持文件名通配符和内容搜索。",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "搜索目录（默认当前目录）",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "文件名模式，支持通配符如 *.py, test*.js（默认 *）",
                        "default": "*",
                    },
                    "content_pattern": {
                        "type": "string",
                        "description": "文件内容模式，在文件中搜索包含此字符串的文件",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "最大结果数量（默认 100）",
                        "default": 100,
                        "minimum": 1,
                        "maximum": 1000,
                    },
                },
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """处理工具调用"""
    if name == "read_file":
        path = arguments.get('path')
        encoding = arguments.get('encoding', 'utf-8')
        if not path:
            raise ValueError("path is required")
        result = read_file(path, encoding)
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]

    elif name == "write_file":
        path = arguments.get('path')
        content = arguments.get('content')
        encoding = arguments.get('encoding', 'utf-8')
        create_dirs = arguments.get('create_dirs', False)
        if not path or content is None:
            raise ValueError("path and content are required")
        result = write_file(path, content, encoding, create_dirs)
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]

    elif name == "search_files":
        directory = arguments.get('directory', os.getcwd())
        pattern = arguments.get('pattern', '*')
        content_pattern = arguments.get('content_pattern')
        max_results = arguments.get('max_results', 100)
        result = search_files(directory, pattern, content_pattern, max_results)
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
