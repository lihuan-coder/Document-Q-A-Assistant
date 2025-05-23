"""
Web应用模块
包含FastAPI应用、WebSocket管理和路由处理
"""

from .websocket_manager import WebSocketManager
from .qa_service import QAService

__all__ = ['WebSocketManager', 'QAService'] 