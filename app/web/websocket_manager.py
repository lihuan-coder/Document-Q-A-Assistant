"""
WebSocket连接管理器
处理WebSocket连接的建立、断开和消息发送
"""

from typing import Set
from fastapi import WebSocket


class WebSocketManager:
    """
    WebSocket连接管理器
    负责管理客户端WebSocket连接和消息传输
    """
    
    def __init__(self):
        """初始化WebSocket管理器"""
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket) -> None:
        """
        接受WebSocket连接
        
        Args:
            websocket: WebSocket连接对象
        """
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"WebSocket连接已建立，当前连接数: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket) -> None:
        """
        断开WebSocket连接
        
        Args:
            websocket: WebSocket连接对象
        """
        self.active_connections.discard(websocket)
        print(f"WebSocket连接已断开，当前连接数: {len(self.active_connections)}")
    
    async def send_json(self, websocket: WebSocket, data: dict) -> None:
        """
        发送JSON数据到客户端
        
        Args:
            websocket: WebSocket连接对象
            data: 要发送的数据字典
        """
        try:
            await websocket.send_json(data)
        except Exception as e:
            print(f"发送JSON数据失败: {e}")
            self.disconnect(websocket)
    
    async def send_text(self, websocket: WebSocket, text: str) -> None:
        """
        发送文本消息到客户端
        
        Args:
            websocket: WebSocket连接对象
            text: 要发送的文本消息
        """
        try:
            await websocket.send_text(text)
        except Exception as e:
            print(f"发送文本消息失败: {e}")
            self.disconnect(websocket)
    
    async def broadcast_json(self, data: dict) -> None:
        """
        向所有连接的客户端广播JSON数据
        
        Args:
            data: 要广播的数据字典
        """
        if not self.active_connections:
            return
            
        disconnected = set()
        for websocket in self.active_connections:
            try:
                await websocket.send_json(data)
            except Exception as e:
                print(f"广播消息失败: {e}")
                disconnected.add(websocket)
        
        # 移除断开的连接
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def broadcast_text(self, text: str) -> None:
        """
        向所有连接的客户端广播文本消息
        
        Args:
            text: 要广播的文本消息
        """
        if not self.active_connections:
            return
            
        disconnected = set()
        for websocket in self.active_connections:
            try:
                await websocket.send_text(text)
            except Exception as e:
                print(f"广播消息失败: {e}")
                disconnected.add(websocket)
        
        # 移除断开的连接
        for websocket in disconnected:
            self.disconnect(websocket)
    
    def get_connection_count(self) -> int:
        """
        获取当前连接数
        
        Returns:
            int: 当前活跃连接数
        """
        return len(self.active_connections)
    
    def is_connected(self, websocket: WebSocket) -> bool:
        """
        检查WebSocket是否仍然连接
        
        Args:
            websocket: WebSocket连接对象
            
        Returns:
            bool: 是否仍然连接
        """
        return websocket in self.active_connections 