"""
问答服务类
整合文档搜索和AI生成功能，提供完整的问答流程
"""

import time
import asyncio
from typing import Dict
from fastapi import WebSocket

from app.services import DocumentSearchService, AIService, KeywordExtractor
from app.web.websocket_manager import WebSocketManager
from config import APP_CONFIG, SEARCH_CONFIG


class QAService:
    """
    问答服务类
    整合文档搜索、关键词提取和AI生成等功能，提供完整的问答流程
    """
    
    def __init__(self):
        """初始化问答服务"""
        # 初始化各个服务组件
        self.document_searcher = DocumentSearchService(
            folder_path=APP_CONFIG["docs_folder"],
            enhanced_context=SEARCH_CONFIG["enhanced_context"]
        )
        self.ai_service = AIService()
        self.keyword_extractor = KeywordExtractor()
        self.ws_manager = WebSocketManager()
        
        print("问答服务已初始化")
    
    async def process_question(self, websocket: WebSocket, question: str) -> None:
        """
        处理用户问题的完整流程
        
        Args:
            websocket: WebSocket连接对象
            question: 用户问题
        """
        start_time = time.time()
        
        try:
            # 第一步：分析问题和提取关键词
            keywords, rewritten = await self._analyze_question(websocket, question)
            
            # 第二步：搜索相关文档（用AI提取的关键词）
            search_results = await self._search_documents(websocket, question, keywords)
            
            # 第三步：生成智能回答
            await self._generate_answer(websocket, question, search_results)
            
            # 发送完成统计信息
            total_time = time.time() - start_time
            await self.ws_manager.send_json(websocket, {
                "step": "completed",
                "message": "问答流程完成",
                "total_time": total_time,
                "results_count": len(search_results)
            })
            
        except Exception as e:
            print(f"处理问题时发生错误: {str(e)}")
            await self.ws_manager.send_json(websocket, {
                "step": "error",
                "message": f"处理问题时发生错误: {str(e)}"
            })
    
    async def _analyze_question(self, websocket: WebSocket, question: str):
        """
        分析问题并提取关键词
        
        Args:
            websocket: WebSocket连接对象
            question: 用户问题
        Returns:
            (keywords, rewritten)
        """
        await self.ws_manager.send_json(websocket, {
            "step": "analyzing",
            "message": "正在分析问题..."
        })
        
        analysis_start_time = time.time()
        
        # ====== 新增：调用千问模型提取关键词和改写问题 ======
        prompt = (
            "请从下列问题中提取5个最重要的关键词，并对问题进行更精炼的改写。"
            "输出格式为：关键词：[关键词1,关键词2,...]；改写：xxx。\n"
            f"问题：{question}"
        )
        qwen_result = await self.ai_service.call_qwen(prompt, max_tokens=256)
        # 解析返回内容
        import re
        keywords = []
        rewritten = ""
        kw_match = re.search(r"关键词\s*[:：]\s*\[(.*?)\]", qwen_result)
        if kw_match:
            keywords = [k.strip() for k in kw_match.group(1).split(',') if k.strip()]
        rewrite_match = re.search(r"改写\s*[:：]\s*(.+)", qwen_result)
        if rewrite_match:
            rewritten = rewrite_match.group(1).strip()
        # ====== 结束 ======
        analysis_time = time.time() - analysis_start_time
        await self.ws_manager.send_json(websocket, {
            "step": "analyzed",
            "message": "问题分析完成",
            "analysis": {
                "question": question,
                "keywords": keywords,
                "keyword_count": len(keywords),
                "rewritten": rewritten
            },
            "time": analysis_time
        })
        print(f"问题分析完成: {question} -> 关键词: {keywords} 改写: {rewritten}")
        return keywords, rewritten
    
    async def _search_documents(self, websocket: WebSocket, question: str, keywords: list) -> list:
        """
        搜索相关文档
        
        Args:
            websocket: WebSocket连接对象
            question: 用户问题
            keywords: AI提取的关键词
        Returns:
            list: 搜索结果列表
        """
        await self.ws_manager.send_json(websocket, {
            "step": "searching",
            "message": "正在搜索文档..."
        })
        
        search_start_time = time.time()
        
        # 直接用AI提取的关键词搜索文档
        search_results = self.document_searcher.search_documents(keywords)
        
        search_time = time.time() - search_start_time
        
        await self.ws_manager.send_json(websocket, {
            "step": "searched",
            "message": f"文档搜索完成，共找到 {len(search_results)} 条相关内容",
            "time": search_time,
            "docs": search_results,
            "docs_count": len(search_results)
        })
        
        # 短暂暂停确保UI更新
        await asyncio.sleep(0.1)
        
        return search_results
    
    async def _generate_answer(self, websocket: WebSocket, question: str, search_results: list) -> None:
        """
        生成智能回答
        
        Args:
            websocket: WebSocket连接对象
            question: 用户问题
            search_results: 搜索结果
        """
        answer_start_time = time.time()
        
        await self.ws_manager.send_json(websocket, {
            "step": "answering",
            "message": "正在生成智能回答...",
            "status": "start"
        })
        
        # 收集完整回答
        answer_chunks = []
        chunk_count = 0
        
        try:
            # 流式生成回答
            async for chunk in self.ai_service.stream_generate_answer(question, search_results):
                if chunk:
                    answer_chunks.append(chunk)
                    chunk_count += 1
                    
                    # 实时发送回答片段
                    await self.ws_manager.send_json(websocket, {
                        "step": "answering",
                        "message": "正在生成智能回答...",
                        "chunk": chunk,
                        "chunk_id": chunk_count
                    })
                    
                    # 短暂暂停确保顺序传输
                    await asyncio.sleep(0.02)
            
            # 计算回答生成时间
            answer_time = time.time() - answer_start_time
            full_answer = "".join(answer_chunks)
            
            # 发送回答完成信号
            await self.ws_manager.send_json(websocket, {
                "step": "answered",
                "message": "回答生成完成",
                "answer": full_answer,
                "time": answer_time,
                "chunk_count": chunk_count
            })
            
            print(f"回答生成完成，共 {chunk_count} 个片段，耗时 {answer_time:.2f}秒")
            
        except Exception as e:
            print(f"生成回答时出错: {str(e)}")
            await self.ws_manager.send_json(websocket, {
                "step": "error",
                "message": f"生成回答时出错: {str(e)}"
            })
    
    def get_service_status(self) -> Dict:
        """
        获取服务状态信息
        
        Returns:
            Dict: 服务状态信息
        """
        return {
            "document_searcher": {
                "folder_path": self.document_searcher.folder_path,
                "cache_info": self.document_searcher.get_cache_info()
            },
            "ai_service": self.ai_service.get_model_info(),
            "websocket_manager": {
                "active_connections": self.ws_manager.get_connection_count()
            }
        }
    
    def clear_caches(self) -> None:
        """清除所有缓存"""
        self.document_searcher.clear_cache()
        print("所有缓存已清除") 