<div align="center">

# 🤖 Smart Document Q&A Assistant

**AI-Powered Document Search and Q&A Application Based on Qwen Large Language Model**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-red.svg)](README.md)

</div>

A modern, intelligent document Q&A system that provides accurate answers by searching through Word documents using AI-powered analysis and semantic understanding.

## ✨ Features

### 🧠 Intelligent Q&A
- **AI-Powered Analysis**: Uses Qwen LLM for question analysis and keyword extraction
- **Semantic Understanding**: Deep semantic analysis with context-aware responses
- **Streaming Output**: Real-time answer generation with progressive display
- **Enhanced Context**: Smart context extraction from document structure

### 🔍 Efficient Search
- **Multi-threaded Processing**: Parallel document processing for faster results
- **Smart Segmentation**: Automatic paragraph and section recognition
- **Similarity Ranking**: Jaccard similarity algorithm for result ranking
- **LRU Caching**: Optimized performance with intelligent caching

### 🌐 Modern Web Interface
- **Responsive Design**: Beautiful UI supporting desktop and mobile
- **Real-time Interaction**: WebSocket-based live Q&A experience
- **Progress Tracking**: Visual progress indicators for all operations
- **Rich Markdown Support**: Comprehensive Markdown rendering with syntax highlighting

### 🛡️ Production Ready
- **Comprehensive Error Handling**: Robust exception handling and recovery
- **Environment Validation**: Automatic system health checks
- **Detailed Logging**: Structured logging with rotation and monitoring
- **Configuration Management**: Flexible configuration with validation

## ⚡ Quick Start

### Prerequisites
- Python 3.7 or higher
- 4GB+ RAM recommended
- 1GB+ available storage

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd Intelligent Document Q&A Assistant
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   ```bash
   # Create .env file
   echo "QWEN_API_KEY=your-actual-api-key-here" > .env
   ```

3. **Add Documents**
   ```bash
   # Place .docx files in data/ folder
   cp your-documents.docx data/
   ```

4. **Run Application**
   ```bash
   python main.py
   # Visit http://localhost:8000
   ```

## 📖 Usage Guide

### Web Interface
1. **Enter Question**: Type your question in the text area
2. **View Progress**: Watch real-time analysis through 4 stages
3. **Review Results**: Browse relevant document segments
4. **Get Answers**: Receive comprehensive AI-generated responses

### Command Line
```bash
python search_cli.py
# Interactive commands: questions, 'clear', 'status', 'quit'
```

## 🔧 Configuration

Key settings in `config.py`:

| Setting | Description | Default |
|---------|-------------|---------|
| `APP_CONFIG.port` | Web server port | 8000 |
| `SEARCH_CONFIG.max_workers` | Parallel threads | 4 |
| `MODEL_CONFIG.temperature` | AI randomness | 0.3 |
| `MODEL_CONFIG.max_tokens` | Response length | 3000 |

## 📚 API Reference

### WebSocket API
- **Endpoint**: `ws://localhost:8000/ws/ask`
- **Message**: `{"question": "your question"}`
- **Response**: Progress updates and streaming answers

### REST API
- `GET /` - Main interface
- `GET /api/status` - System status
- `POST /api/clear-cache` - Clear caches

## 🚀 Deployment

### Docker
```bash
docker build -t smart-qa-system .
docker run -p 8000:8000 -v ./data:/app/data -e QWEN_API_KEY=your-key smart-qa-system
```

### Production
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 💻 Contributor
<a href="https://github.com/lihuan-coder/Document_QA_Assistant/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=lihuan-coder/Document_QA_Assistant" />
</a>


## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this project if it helps you!**

</div>
