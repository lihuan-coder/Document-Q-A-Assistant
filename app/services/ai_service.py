"""
AI服务模块
提供基于千问大模型的智能问答服务
"""

import json
import asyncio
from typing import List, Dict, AsyncGenerator
from dashscope import Generation
from config import API_KEY, MODEL_CONFIG


class AIService:
    """
    AI智能问答服务
    基于千问大模型提供文档问答功能
    """
    
    def __init__(self, api_key: str = None):
        """
        初始化AI服务
        
        Args:
            api_key: API密钥，如果为None则使用配置文件中的密钥
        """
        self.api_key = api_key or API_KEY
        self.model_config = MODEL_CONFIG.copy()
    
    async def stream_generate_answer(self, question: str, search_results: List[Dict]) -> AsyncGenerator[str, None]:
        """
        流式生成问答结果
        
        Args:
            question: 用户问题
            search_results: 文档搜索结果
            
        Yields:
            str: 生成的回答片段
        """
        if not search_results:
            yield "抱歉，没有找到相关的文档内容来回答您的问题。"
            return
            
        try:
            # 准备输入数据，只选择最相关的前5个结果
            sorted_results = sorted(
                search_results, 
                key=lambda x: len(x.get('关键词', [])), 
                reverse=True
            )[:5]
            
            # 构建详细的提示词
            prompt = self._build_prompt(question, sorted_results)
            
            # 调用千问API进行流式生成
            response = Generation.call(
                model="qwen-plus",  # 使用稳定的模型版本
                prompt=prompt,
                temperature=0.3,    # 降低温度提高一致性
                max_tokens=3000,    # 增加最大token数
                top_p=0.8,
                result_format="message",
                api_key=self.api_key,
                stream=True
            )
            
            if response:
                last_content = ""
                
                # 逐块处理响应
                for chunk in response:
                    try:
                        if chunk and hasattr(chunk, 'output'):
                            content = chunk.output.choices[0].message.content
                            
                            if content and content != last_content:
                                # 计算新增内容
                                new_content = content[len(last_content):]
                                if new_content:
                                    yield new_content
                                    # 短暂暂停以确保顺序传输
                                    await asyncio.sleep(0.01)
                                last_content = content
                                
                    except Exception as e:
                        print(f"处理AI响应块时出错: {e}")
                        continue
                
                # 如果没有收到任何内容，提供默认回答
                if not last_content:
                    yield "## 回答生成中断\n\n抱歉，回答生成过程中断。请重新提问。"
            else:
                yield "## 无法生成回答\n\n抱歉，无法连接到AI模型服务。请稍后再试。"
                
        except Exception as e:
            print(f"AI生成回答时发生错误: {str(e)}")
            error_message = (f"## 处理出错\n\n"
                           f"生成回答时发生错误: {str(e)}\n\n"
                           f"请联系系统管理员或稍后重试。")
            yield error_message
    
    def _build_prompt(self, question: str, search_results: List[Dict]) -> str:
        """
        构建AI模型的输入提示词
        
        Args:
            question: 用户问题
            search_results: 搜索结果
            
        Returns:
            str: 构建的提示词
        """
        prompt = f"""请作为专业的智能文档分析助手，根据以下文档内容回答用户的问题。

用户问题：{question}

相关文档内容：
{json.dumps(search_results, ensure_ascii=False, indent=2)}

请按以下要求回答：
1. 以二级标题"## 回答摘要"开始，先简要概括1-2句要点
2. 在"## 详细解析"部分详细分析问题
3. 保持专业性，引用文档原文并给出具体解决方案
4. 结构清晰，条理分明，易于阅读
5. 使用Markdown格式，如列表、强调等，但不要使用表格、图片等复杂元素
6. 回答完整，不要省略或截断内容，确保所有要点都被覆盖
7. 直接输出UTF-8中文，不使用Unicode转义
8. 务必完整回答，不要在中途停止，如果内容较长请确保结构完整
9. 最后以"## 总结"结束，提供简明的操作建议

请严格按照上述格式要求回答，确保回答的专业性和完整性。"""
        
        return prompt
    
    def validate_api_key(self) -> bool:
        """
        验证API密钥是否有效
        
        Returns:
            bool: API密钥是否有效
        """
        if not self.api_key or self.api_key == "your-api-key-here":
            return False
            
        try:
            # 发送一个简单的测试请求
            response = Generation.call(
                model="qwen-turbo",
                prompt="你好",
                max_tokens=10,
                api_key=self.api_key
            )
            return response is not None
        except Exception as e:
            print(f"API密钥验证失败: {e}")
            return False
    
    def get_model_info(self) -> Dict:
        """
        获取当前模型配置信息
        
        Returns:
            Dict: 模型配置信息
        """
        return {
            "model": "qwen-plus",
            "api_key_valid": self.validate_api_key(),
            "config": self.model_config
        }
    
    def update_config(self, **kwargs) -> None:
        """
        更新模型配置
        
        Args:
            **kwargs: 配置参数
        """
        for key, value in kwargs.items():
            if key in self.model_config:
                self.model_config[key] = value
                print(f"已更新配置 {key} = {value}")
    
    async def call_qwen(self, prompt: str, **kwargs) -> str:
        """
        通用千问API调用，返回完整输出
        Args:
            prompt: 输入提示词
            **kwargs: 其他模型参数
        Returns:
            str: 千问模型输出
        """
        loop = asyncio.get_event_loop()
        params = {
            "model": kwargs.get("model", self.model_config.get("model", "qwen-plus")),
            "prompt": prompt,
            "temperature": kwargs.get("temperature", self.model_config.get("temperature", 0.3)),
            "max_tokens": kwargs.get("max_tokens", self.model_config.get("max_tokens", 300)),
            "top_p": kwargs.get("top_p", self.model_config.get("top_p", 0.8)),
            "result_format": kwargs.get("result_format", "message"),
            "api_key": self.api_key,
            "stream": False
        }
        try:
            response = await loop.run_in_executor(None, lambda: Generation.call(**params))
            if response and hasattr(response, 'output'):
                return response.output.choices[0].message.content
            return ""
        except Exception as e:
            print(f"千问API调用失败: {e}")
            return "" 