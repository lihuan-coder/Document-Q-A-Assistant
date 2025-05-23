"""
日志配置工具
设置应用程序的日志记录
"""

import logging
import sys
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str = "smart_qa_system", 
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    设置应用程序日志记录器
    
    Args:
        name: 日志器名称
        level: 日志级别
        log_file: 日志文件路径，如果为None则只输出到控制台
        
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 如果指定了日志文件，添加文件处理器
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"无法创建日志文件 {log_file}: {e}")
    
    return logger


def get_logger(name: str = "smart_qa_system") -> logging.Logger:
    """
    获取已配置的日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        logging.Logger: 日志器实例
    """
    return logging.getLogger(name)


class RequestLogger:
    """
    请求日志记录器
    用于记录HTTP请求和WebSocket连接
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        初始化请求日志记录器
        
        Args:
            logger: 日志器实例，如果为None则创建新的
        """
        self.logger = logger or get_logger("request_logger")
    
    def log_http_request(self, method: str, path: str, status_code: int, 
                        duration: float, client_ip: str = None) -> None:
        """
        记录HTTP请求日志
        
        Args:
            method: HTTP方法
            path: 请求路径
            status_code: 状态码
            duration: 请求处理时间（秒）
            client_ip: 客户端IP地址
        """
        client_info = f" - {client_ip}" if client_ip else ""
        self.logger.info(
            f"HTTP {method} {path} - {status_code} - {duration:.3f}s{client_info}"
        )
    
    def log_websocket_connection(self, action: str, client_ip: str = None, 
                               connection_count: int = None) -> None:
        """
        记录WebSocket连接日志
        
        Args:
            action: 动作类型（connect/disconnect）
            client_ip: 客户端IP地址
            connection_count: 当前连接数
        """
        client_info = f" - {client_ip}" if client_ip else ""
        count_info = f" - 连接数: {connection_count}" if connection_count is not None else ""
        self.logger.info(f"WebSocket {action}{client_info}{count_info}")
    
    def log_question_processing(self, question: str, keywords: list, 
                              search_results_count: int, duration: float) -> None:
        """
        记录问题处理日志
        
        Args:
            question: 用户问题
            keywords: 提取的关键词
            search_results_count: 搜索结果数量
            duration: 处理时间（秒）
        """
        self.logger.info(
            f"问题处理: '{question}' - 关键词: {keywords} - "
            f"结果数: {search_results_count} - 耗时: {duration:.3f}s"
        )


class PerformanceLogger:
    """
    性能日志记录器
    用于记录系统性能指标
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        初始化性能日志记录器
        
        Args:
            logger: 日志器实例，如果为None则创建新的
        """
        self.logger = logger or get_logger("performance_logger")
    
    def log_search_performance(self, keywords: list, file_count: int, 
                             results_count: int, duration: float) -> None:
        """
        记录搜索性能日志
        
        Args:
            keywords: 搜索关键词
            file_count: 搜索的文件数量
            results_count: 搜索结果数量
            duration: 搜索耗时（秒）
        """
        self.logger.info(
            f"搜索性能: 关键词数={len(keywords)}, 文件数={file_count}, "
            f"结果数={results_count}, 耗时={duration:.3f}s"
        )
    
    def log_ai_generation_performance(self, question_length: int, 
                                    results_count: int, response_chunks: int, 
                                    duration: float) -> None:
        """
        记录AI生成性能日志
        
        Args:
            question_length: 问题长度
            results_count: 输入的搜索结果数量
            response_chunks: 响应块数量
            duration: 生成耗时（秒）
        """
        self.logger.info(
            f"AI生成性能: 问题长度={question_length}, 输入结果数={results_count}, "
            f"响应块数={response_chunks}, 耗时={duration:.3f}s"
        )
    
    def log_cache_performance(self, cache_type: str, hit: bool, size: int) -> None:
        """
        记录缓存性能日志
        
        Args:
            cache_type: 缓存类型
            hit: 是否命中缓存
            size: 缓存大小
        """
        status = "命中" if hit else "未命中"
        self.logger.debug(f"缓存{status}: {cache_type} - 缓存大小: {size}")


# 预配置的日志器实例
main_logger = setup_logger("smart_qa_system")
request_logger = RequestLogger()
performance_logger = PerformanceLogger() 