#!/usr/bin/env python3
"""
File Operations MCP Server 测试

运行方式: python test.py
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from server import read_file, write_file, search_files, is_path_allowed

# 颜色输出
class Colors:
    RESET = '\033[0m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    BLUE = '\033[36m'


def log(name: str, status: str, message: str = ''):
    status_color = Colors.GREEN if status == 'PASS' else Colors.RED
    print(f"{Colors.BLUE}[TEST]{Colors.RESET} {name}: {status_color}{status}{Colors.RESET} {message}")


def run_tests():
    print('\n=== File Operations MCP 测试套件 ===\n')

    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_content = "Hello, MCP!\nThis is a test file."

        tests = [
            {
                'name': '写入文件',
                'fn': lambda: write_file(str(test_file), test_content),
            },
            {
                'name': '读取文件',
                'fn': lambda: read_file(str(test_file)),
            },
            {
                'name': '搜索文件',
                'fn': lambda: search_files(tmpdir, '*.txt'),
            },
            {
                'name': '内容搜索',
                'fn': lambda: search_files(tmpdir, '*', 'MCP'),
            },
            {
                'name': '创建目录并写入',
                'fn': lambda: write_file(
                    str(Path(tmpdir) / 'subdir' / 'nested.txt'),
                    'nested content',
                    create_dirs=True
                ),
            },
        ]

        passed = 0
        failed = 0

        for test in tests:
            try:
                result = test.fn()

                if 'error' in result:
                    raise ValueError(result['error'])

                # 验证写入
                if test['name'] == '写入文件':
                    if not result.get('success'):
                        raise ValueError('写入未标记为成功')
                    if not test_file.exists():
                        raise ValueError('文件未创建')
                    log(test['name'], 'PASS', f'写入 {result.get("bytes_written", 0)} 字节')

                # 验证读取
                elif test['name'] == '读取文件':
                    if result.get('content') != test_content:
                        raise ValueError('内容不匹配')
                    log(test['name'], 'PASS', f'读取 {result.get("line_count")} 行')

                # 验证搜索
                elif test['name'] == '搜索文件':
                    count = result.get('count', 0)
                    if count == 0:
                        raise ValueError('未找到文件')
                    log(test['name'], 'PASS', f'找到 {count} 个文件')

                # 验证内容搜索
                elif test['name'] == '内容搜索':
                    count = result.get('count', 0)
                    if count == 0:
                        raise ValueError('未找到匹配')
                    results = result.get('results', [])
                    if results and 'matches' not in results[0]:
                        raise ValueError('缺少匹配信息')
                    log(test['name'], 'PASS', f'在 {count} 个文件中找到匹配')

                # 验证嵌套创建
                elif test['name'] == '创建目录并写入':
                    nested_file = Path(tmpdir) / 'subdir' / 'nested.txt'
                    if not nested_file.exists():
                        raise ValueError('嵌套文件未创建')
                    log(test['name'], 'PASS', '成功创建嵌套目录')

                passed += 1

            except Exception as e:
                log(test['name'], 'FAIL', str(e))
                failed += 1

        # 测试错误处理
        error_tests = [
            {
                'name': '读取不存在的文件',
                'fn': lambda: read_file(str(Path(tmpdir) / 'nonexistent.txt')),
                'should_error': True,
            },
            {
                'name': '路径安全检查（系统文件）',
                'fn': lambda: is_path_allowed('/etc/passwd'),
                'should_error': False,  # 不应该抛出异常，但返回 False
            },
        ]

        for test in error_tests:
            try:
                result = test['fn']()
                has_error = 'error' in result or result is False

                if test['should_error']:
                    if not has_error:
                        log(test['name'], 'FAIL', '应该返回错误但没有')
                        failed += 1
                    else:
                        log(test['name'], 'PASS', '正确返回错误')
                        passed += 1
                else:
                    if isinstance(result, bool) and not result:
                        log(test['name'], 'PASS', '正确拒绝系统路径')
                        passed += 1
                    elif has_error:
                        log(test['name'], 'PASS', '正确返回错误')
                        passed += 1
                    else:
                        log(test['name'], 'FAIL', '未按预期处理')
                        failed += 1

            except Exception as e:
                log(test['name'], 'FAIL', f'意外异常: {e}')
                failed += 1

    print(f'\n=== 测试结果: {passed} 通过, {failed} 失败 ===\n')

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    run_tests()
