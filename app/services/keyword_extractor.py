"""
关键词提取服务
使用jieba分词进行中文关键词提取
"""

import jieba
import re
from typing import List
from config import STOPWORDS


class KeywordExtractor:
    """
    关键词提取器
    使用jieba分词工具进行中文文本的关键词提取
    """
    
    def __init__(self, stopwords: set = None):
        """
        初始化关键词提取器
        
        Args:
            stopwords: 停用词集合，如果为None则使用默认停用词
        """
        self.stopwords = stopwords or STOPWORDS
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        从文本中提取关键词
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 提取的关键词列表（已去重）
        """
        if not text or not text.strip():
            return []
            
        # 使用jieba进行分词
        words = jieba.lcut(text)
        
        # 过滤关键词
        keywords = []
        for word in words:
            word = word.strip()
            if self._is_valid_keyword(word):
                keywords.append(word)
        
        # 去重并保持顺序
        return list(dict.fromkeys(keywords))
    
    def _is_valid_keyword(self, word: str) -> bool:
        """
        判断词汇是否为有效关键词
        
        Args:
            word: 待判断的词汇
            
        Returns:
            bool: 是否为有效关键词
        """
        if not word:
            return False
            
        # 过滤空白字符
        if not word.strip():
            return False
            
        # 过滤停用词
        if word in self.stopwords:
            return False
            
        # 只保留包含中文、英文或数字的词汇
        if not re.match(r'[\u4e00-\u9fa5a-zA-Z0-9]', word):
            return False
            
        # 过滤单个字符（除非是数字）
        if len(word) == 1 and not word.isdigit():
            return False
            
        return True
    
    def add_stopwords(self, words: List[str]) -> None:
        """
        添加停用词
        
        Args:
            words: 要添加的停用词列表
        """
        self.stopwords.update(words)
    
    def remove_stopwords(self, words: List[str]) -> None:
        """
        移除停用词
        
        Args:
            words: 要移除的停用词列表
        """
        for word in words:
            self.stopwords.discard(word) 