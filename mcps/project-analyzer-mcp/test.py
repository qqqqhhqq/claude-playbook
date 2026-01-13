#!/usr/bin/env python3
"""
Project Analyzer MCP Server 测试

运行方式: python test.py
"""

import json
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from server import analyze_directory, count_lines, list_dependencies

# 颜色输出
class Colors:
    RESET = '\033[0m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    BLUE = '\033[36m'
    YELLOW = '\033[33m'


def log(name: str, status: str, message: str = ''):
    status_color = Colors.GREEN if status == 'PASS' else Colors.RED
    print(f"{Colors.BLUE}[TEST]{Colors.RESET} {name}: {status_color}{status}{Colors.RESET} {message}")


def run_tests():
    print('\n=== Project Analyzer MCP 测试套件 ===\n')

    # 测试目录
    test_dir = Path(__file__).parent.parent.parent

    tests = [
        {
            'name': '目录结构分析',
            'fn': lambda: analyze_directory(str(test_dir), 2),
        },
        {
            'name': '代码行数统计',
            'fn': lambda: count_lines(str(test_dir)),
        },
        {
            'name': '依赖列表',
            'fn': lambda: list_dependencies(str(test_dir)),
        },
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            result = test.fn()

            # 验证结果
            if isinstance(result, dict):
                if 'error' in result:
                    raise ValueError(result['error'])

                log(test['name'], 'PASS', f'返回结果类型: {type(result).__name__}')

                # 打印部分结果
                if test['name'] == '目录结构分析':
                    print(f'  ├─ 根目录: {result.get("name", "N/A")}')
                elif test['name'] == '代码行数统计':
                    print(f'  ├─ 总文件数: {result.get("total_files", 0)}')
                    print(f'  └─ 总行数: {result.get("total_lines", 0)}')
                elif test['name'] == '依赖列表':
                    managers = result.get('dependency_managers', [])
                    print(f'  └─ 检测到的包管理器: {", ".join(managers) if managers else "无"}')

                passed += 1
            else:
                raise ValueError(f'返回结果不是字典: {type(result)}')

        except Exception as e:
            log(test['name'], 'FAIL', str(e))
            failed += 1

    # 额外测试：测试不存在的路径
    try:
        result = analyze_directory('/nonexistent/path/12345')
        if 'error' not in result:
            log('错误处理测试', 'FAIL', '应该返回错误但没有')
            failed += 1
        else:
            log('错误处理测试', 'PASS', '正确处理不存在的路径')
            passed += 1
    except Exception as e:
        log('错误处理测试', 'FAIL', str(e))
        failed += 1

    print(f'\n=== 测试结果: {passed} 通过, {failed} 失败 ===\n')

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    run_tests()
