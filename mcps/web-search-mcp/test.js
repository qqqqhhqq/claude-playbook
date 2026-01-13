#!/usr/bin/env node

/**
 * Web Search MCP Server 测试
 *
 * 运行方式: node test.js
 */

import { searchWeb } from './server.js';

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
};

function log(name, status, message) {
  const statusColor = status === 'PASS' ? colors.green : colors.red;
  console.log(`${colors.blue}[TEST]${colors.reset} ${name}: ${statusColor}${status}${colors.reset} ${message ? '- ' + message : ''}`);
}

async function runTests() {
  console.log('\n=== Web Search MCP 测试套件 ===\n');

  const tests = [
    {
      name: '基础搜索',
      fn: async () => {
        const result = await searchWeb('TypeScript', 3);
        if (!result.results || result.results.length === 0) {
          throw new Error('No results returned');
        }
        return result;
      },
    },
    {
      name: '中文搜索',
      fn: async () => {
        const result = await searchWeb('人工智能', 3);
        if (!result.results || result.results.length === 0) {
          throw new Error('No results returned');
        }
        return result;
      },
    },
    {
      name: '技术文档搜索',
      fn: async () => {
        const result = await searchWeb('Node.js fs module', 3);
        if (!result.results || result.results.length === 0) {
          throw new Error('No results returned');
        }
        return result;
      },
    },
  ];

  let passed = 0;
  let failed = 0;

  for (const test of tests) {
    try {
      const result = await test.fn();
      log(test.name, 'PASS', `找到 ${result.results.length} 条结果`);
      passed++;
    } catch (error) {
      log(test.name, 'FAIL', error.message);
      failed++;
    }
  }

  console.log(`\n=== 测试结果: ${passed} 通过, ${failed} 失败 ===\n`);

  process.exit(failed > 0 ? 1 : 0);
}

// 导出测试函数以便 server.js 可以导入 searchWeb
// 注意：需要在 server.js 中导出 searchWeb 函数

runTests().catch((error) => {
  console.error('测试运行失败:', error);
  process.exit(1);
});
