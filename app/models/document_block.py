"""
文档块数据模型
用于存储和处理文档块信息
"""

from typing import List, Dict


class DocumentBlock:
    """
    文档块类，用于存储和处理文档块信息
    
    Attributes:
        filename (str): 文件名
        content (str): 块内容
        context (str): 上下文信息（如标题）
        start_index (int): 起始段落索引
        keywords (List[str]): 匹配的关键词列表
        similarity_score (float): 相似度分数
    """
    
    def __init__(self, filename: str, content: str, context: str, 
                 start_index: int, keywords: List[str]):
        """
        初始化文档块
        
        Args:
            filename: 文件名
            content: 块内容
            context: 上下文信息
            start_index: 起始段落索引
            keywords: 匹配的关键词列表
        """
        self.filename = filename
        self.content = content
        self.context = context
        self.start_index = start_index
        self.keywords = keywords
        self.similarity_score = 0.0

    def to_dict(self) -> Dict:
        """
        将文档块对象转换为字典格式
        
        Returns:
            Dict: 包含文档块信息的字典
        """
        return {
            "文件名": self.filename,
            "关键词": self.keywords,
            "上下文": self.context,
            "文段起始段落号": self.start_index + 1,
            "内容": self.content
        }
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"DocumentBlock(file={self.filename}, start={self.start_index}, keywords={len(self.keywords)})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return (f"DocumentBlock(filename='{self.filename}', "
                f"start_index={self.start_index}, "
                f"keywords={self.keywords}, "
                f"similarity_score={self.similarity_score})") 