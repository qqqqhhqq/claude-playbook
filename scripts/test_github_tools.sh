#!/bin/bash
# GitHub 代码分析器 - 功能测试脚本

set -e

echo "=========================================="
echo "GitHub 代码分析器 - 功能测试"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试仓库
TEST_REPO="vitejs/vite"
TEST_BRANCH="main"

echo -e "${YELLOW}测试仓库: ${TEST_REPO}${NC}"
echo ""

# 测试 1: 获取仓库信息
echo "=========================================="
echo "测试 1: 获取仓库信息"
echo "=========================================="
if python3 scripts/github_get_repo_info.py "$TEST_REPO" > /tmp/test_repo_info.json 2>&1; then
    echo -e "${GREEN}✓ 获取仓库信息成功${NC}"
    echo "仓库名称: $(cat /tmp/test_repo_info.json | grep -o '"name": "[^"]*"' | cut -d'"' -f4)"
    echo "语言: $(cat /tmp/test_repo_info.json | grep -o '"language": "[^"]*"' | cut -d'"' -f4)"
else
    echo -e "${RED}✗ 获取仓库信息失败${NC}"
    cat /tmp/test_repo_info.json
fi
echo ""

# 测试 2: 获取目录结构
echo "=========================================="
echo "测试 2: 获取目录结构"
echo "=========================================="
if python3 scripts/github_get_repo_structure.py "$TEST_REPO" > /tmp/test_structure.json 2>&1; then
    echo -e "${GREEN}✓ 获取目录结构成功${NC}"
    TOTAL_COUNT=$(cat /tmp/test_structure.json | grep -o '"total_count": [0-9]*' | cut -d' ' -f2)
    echo "根目录文件数: $TOTAL_COUNT"
else
    echo -e "${RED}✗ 获取目录结构失败${NC}"
    cat /tmp/test_structure.json
fi
echo ""

# 测试 3: 读取文件内容
echo "=========================================="
echo "测试 3: 读取 README 文件"
echo "=========================================="
if python3 scripts/github_read_file.py "$TEST_REPO" "README.md" > /tmp/test_readme.json 2>&1; then
    echo -e "${GREEN}✓ 读取 README 成功${NC}"
    SIZE=$(cat /tmp/test_readme.json | grep -o '"size": [0-9]*' | cut -d' ' -f2)
    echo "文件大小: $SIZE 字节"
    TRUNCATED=$(cat /tmp/test_readme.json | grep -o '"truncated": [a-z]*' | cut -d' ' -f2)
    if [ "$TRUNCATED" = "true" ]; then
        echo -e "${YELLOW}⚠ 文件已被截断${NC}"
    fi
else
    echo -e "${RED}✗ 读取 README 失败${NC}"
    cat /tmp/test_readme.json
fi
echo ""

# 测试 4: 搜索代码
echo "=========================================="
echo "测试 4: 搜索代码关键词 'plugin'"
echo "=========================================="
if python3 scripts/github_search_code.py "$TEST_REPO" "plugin" "$TEST_BRANCH" > /tmp/test_search.json 2>&1; then
    echo -e "${GREEN}✓ 搜索代码成功${NC}"
    TOTAL_COUNT=$(cat /tmp/test_search.json | grep -o '"total_count": [0-9]*' | cut -d' ' -f2)
    echo "匹配文件数: $TOTAL_COUNT"
    RESULT_COUNT=$(cat /tmp/test_search.json | grep -o '"count": [0-9]*' | cut -d' ' -f2)
    echo "返回结果数: $RESULT_COUNT"
else
    echo -e "${RED}✗ 搜索代码失败${NC}"
    cat /tmp/test_search.json
fi
echo ""

# 总结
echo "=========================================="
echo "测试完成"
echo "=========================================="
echo ""
echo "临时文件位置:"
echo "  - /tmp/test_repo_info.json"
echo "  - /tmp/test_structure.json"
echo "  - /tmp/test_readme.json"
echo "  - /tmp/test_search.json"
echo ""
echo "查看示例："
echo "  cat /tmp/test_repo_info.json | jq"
