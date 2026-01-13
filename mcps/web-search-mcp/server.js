#!/usr/bin/env node

/**
 * Web Search MCP Server
 *
 * 提供联网搜索功能的 MCP 服务器，使用 DuckDuckGo Instant Answer API
 * 无需 API key，免费使用
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// DuckDuckGo Instant Answer API
const DUCKDUCKGO_API = 'https://api.duckduckgo.com/';

/**
 * 执行网络搜索
 * @param {string} query - 搜索查询
 * @param {number} limit - 返回结果数量限制
 * @returns {Promise<Object>} 搜索结果
 */
async function searchWeb(query, limit = 5) {
  const params = new URLSearchParams({
    q: query,
    format: 'json',
    no_html: '1',
    skip_disambig: '1',
  });

  try {
    const response = await fetch(`${DUCKDUCKGO_API}?${params}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    const data = await response.json();

    // 构建结果
    const results = [];

    // 添加主要答案
    if (data.Abstract) {
      results.push({
        title: data.Heading || 'DuckDuckGo Answer',
        url: data.AbstractURL || data.AbstractSource || '',
        snippet: data.Abstract,
      });
    }

    // 添加相关主题
    if (data.RelatedTopics && Array.isArray(data.RelatedTopics)) {
      for (const topic of data.RelatedTopics) {
        if (topic.Text && topic.FirstURL && results.length < limit) {
          results.push({
            title: topic.Text.split(' - ')[0].substring(0, 80),
            url: topic.FirstURL,
            snippet: topic.Text,
          });
        }
      }
    }

    // 添加外部结果
    if (data.Results && Array.isArray(data.Results)) {
      for (const result of data.Results) {
        if (result.Text && result.FirstURL && results.length < limit) {
          results.push({
            title: result.Text,
            url: result.FirstURL,
            snippet: result.Text,
          });
        }
      }
    }

    return {
      query,
      count: results.length,
      results: results.length > 0 ? results : [{ title: 'No results', url: '', snippet: 'No results found for the query.' }],
    };
  } catch (error) {
    return {
      query,
      error: error.message,
      results: [],
    };
  }
}

// 创建 MCP 服务器
const server = new Server(
  {
    name: 'web-search-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 列出可用工具
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'search_web',
        description: '在互联网上搜索信息，返回相关结果摘要。适用于查找最新资讯、技术文档、定义解释等。',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: '搜索查询字符串',
            },
            limit: {
              type: 'number',
              description: '返回结果的最大数量（默认 5，最大 10）',
              default: 5,
              minimum: 1,
              maximum: 10,
            },
          },
          required: ['query'],
        },
      },
    ],
  };
});

// 处理工具调用
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'search_web') {
    const query = args?.query;
    const limit = Math.min(args?.limit || 5, 10);

    if (!query || typeof query !== 'string') {
      throw new Error('Invalid query: must be a non-empty string');
    }

    const result = await searchWeb(query, limit);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.stderr('Web Search MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
