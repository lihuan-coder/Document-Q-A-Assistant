<div align="center">

# 🤖 智能文档问答助手

**基于千问大模型的智能文档搜索与问答应用**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-red.svg)](README.md)

</div>

一款现代化的智能文档问答系统，通过AI驱动的分析和语义理解，在Word文档中搜索并提供准确答案。

## ✨ 核心功能

### 🧠 智能问答
- **AI驱动分析**：使用千问大模型进行问题分析和关键词提取
- **语义理解**：深度语义分析与上下文感知回答
- **流式输出**：实时答案生成，逐步显示回答内容
- **增强上下文**：智能提取文档结构和上下文信息

### 🔍 高效搜索
- **多线程处理**：并行文档处理，提升搜索速度
- **智能分段**：自动段落和章节识别
- **相似度排序**：Jaccard相似度算法排序结果
- **LRU缓存**：智能缓存优化，提升性能

### 🌐 现代化界面
- **响应式设计**：支持桌面和移动端的美观界面
- **实时交互**：基于WebSocket的实时问答体验
- **进度跟踪**：可视化进度指示器显示处理状态
- **丰富Markdown**：全面的Markdown渲染和语法高亮

### 🛡️ 生产就绪
- **全面错误处理**：健壮的异常处理和恢复机制
- **环境验证**：自动系统健康检查
- **详细日志**：结构化日志记录与轮转监控
- **配置管理**：灵活的配置管理和验证

## ⚡ 快速开始

### 系统要求
- Python 3.7 或更高版本
- 内存：建议4GB以上
- 存储：可用空间1GB以上
- 操作系统：Windows/Linux/macOS

### 安装步骤

1. **克隆项目并安装**
   ```bash
   下载项目文件
   cd Intelligent Document Q&A Assistant
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或 venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **配置API密钥**
   ```bash
   # 创建.env文件
   echo "QWEN_API_KEY=你的实际API密钥" > .env
   ```
   
   > 获取千问API密钥：访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)

3. **添加文档**
   ```bash
   将.docx文件放入data/文件夹
   ```

4. **运行应用**
   ```bash
   python main.py
   # 访问 http://localhost:8000
   ```

## 📖 使用指南

### Web界面操作流程

1. **输入问题**：在文本框中输入您的问题
2. **观察进度**：实时观看4个阶段的分析进度
   - 📝 问题分析：AI提取关键词并改写问题
   - 🔍 文档搜索：并行搜索相关文档段落
   - 🤖 生成回答：流式生成智能回答
   - ✅ 完成：显示统计信息
3. **查看结果**：浏览相关文档片段
4. **获得答案**：阅读AI生成的全面回答

### 命令行工具

```bash
python search_cli.py

# 可用命令：
# - 输入问题进行搜索
# - 'clear' - 清除搜索缓存
# - 'status' - 显示系统状态
# - 'quit' 或 'exit' - 退出程序
```

**示例使用：**
```bash
🤔 请输入您的问题: 如何配置服务器？
🏷️ 提取的关键词: 配置, 服务器, 设置, 安装
📚 正在搜索文档...
📋 搜索结果 (共找到 3 条):
...
💾 详细结果已保存到: search_results.json
```

## 🔧 配置详解

### 核心配置项（config.py）

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `APP_CONFIG.port` | Web服务器端口 | 8000 |
| `APP_CONFIG.docs_folder` | 文档文件夹路径 | "data" |
| `SEARCH_CONFIG.max_workers` | 并行处理线程数 | 4 |
| `SEARCH_CONFIG.max_results` | 最大搜索结果数 | 10 |
| `MODEL_CONFIG.temperature` | AI模型随机性 | 0.3 |
| `MODEL_CONFIG.max_tokens` | 最大输出token数 | 3000 |

### 性能优化建议

#### 搜索性能优化
```python
SEARCH_CONFIG = {
    "max_workers": 8,           # 增加并行线程，适合多核CPU
    "cache_size": 200,          # 增大缓存，提升重复查询性能
    "enhanced_context": True,   # 启用增强上下文模式
}
```

#### AI模型调优
```python
MODEL_CONFIG = {
    "temperature": 0.3,         # 降低随机性，提高答案一致性
    "max_tokens": 4000,         # 增加长度限制，支持更详细回答
    "top_p": 0.8,              # 控制输出多样性
}
```

## 📚 API接口文档

### WebSocket API
- **端点**：`ws://localhost:8000/ws/ask`
- **消息格式**：`{"question": "用户问题"}`
- **响应阶段**：分析中 → 搜索中 → 回答中 → 完成

### REST API
- `GET /` - 主应用界面
- `GET /api/status` - 系统状态信息
- `POST /api/clear-cache` - 清除系统缓存

## 🚀 部署方案

### Docker部署
```bash
docker build -t smart-qa-system .
docker run -p 8000:8000 -v ./data:/app/data -e QWEN_API_KEY=你的密钥 smart-qa-system
```

### 生产环境部署
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Nginx配置示例
```nginx
server {
    listen 80;
    server_name 你的域名.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 🔍 工作原理

### 1. 问题分析阶段
```
用户输入 → AI分析 → 关键词提取 → 问题改写
```
- 使用千问大模型提取有意义的关键词
- 改写问题以提高搜索准确性
- 识别用户意图和上下文

### 2. 文档搜索阶段
```
关键词 → 文档解析 → 上下文提取 → 相似度排序
```
- 多线程并行文档处理
- 智能段落分割
- 层级上下文提取
- Jaccard相似度评分

### 3. 回答生成阶段
```
搜索结果 → 提示词构建 → AI生成 → 流式输出
```
- 智能提示词工程
- 流式响应生成
- Markdown格式化
- 全面的回答结构

## 📄 开源协议

本项目基于MIT协议开源 - 详见[LICENSE](LICENSE)文件。

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个星标！**

</div>
