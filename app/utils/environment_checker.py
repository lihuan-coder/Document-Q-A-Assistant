"""
环境检查工具
检查运行环境和配置是否正确
"""

import os
from typing import List, Dict, Tuple
from config import APP_CONFIG, API_KEY


class EnvironmentChecker:
    """
    环境检查器
    检查应用运行所需的环境配置和依赖
    """
    
    def __init__(self):
        """初始化环境检查器"""
        self.errors = []
        self.warnings = []
        self.info = []
    
    def check_all(self) -> Tuple[bool, Dict]:
        """
        执行全面的环境检查
        
        Returns:
            Tuple[bool, Dict]: (是否通过检查, 检查结果详情)
        """
        self.errors.clear()
        self.warnings.clear()
        self.info.clear()
        
        # 检查API密钥
        self._check_api_key()
        
        # 检查目录结构
        self._check_directories()
        
        # 检查文档文件夹
        self._check_docs_folder()
        
        # 检查端口可用性
        self._check_port()
        
        # 整理检查结果
        is_passed = len(self.errors) == 0
        result = {
            "passed": is_passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info
        }
        
        return is_passed, result
    
    def _check_api_key(self) -> None:
        """检查API密钥配置"""
        if not API_KEY or API_KEY == "your-api-key-here":
            self.errors.append({
                "type": "api_key",
                "message": "未设置QWEN_API_KEY环境变量",
                "solution": [
                    "创建.env文件并添加：QWEN_API_KEY=your-api-key",
                    "或在运行前设置环境变量：set QWEN_API_KEY=your-api-key (Windows)"
                ]
            })
        else:
            self.info.append({
                "type": "api_key",
                "message": "API密钥配置正常"
            })
    
    def _check_directories(self) -> None:
        """检查必要的目录结构"""
        required_dirs = [
            (APP_CONFIG["templates_dir"], "模板目录"),
            (APP_CONFIG["static_dir"], "静态文件目录")
        ]
        
        for dir_path, dir_name in required_dirs:
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path, exist_ok=True)
                    self.info.append({
                        "type": "directory",
                        "message": f"已创建{dir_name}: {dir_path}"
                    })
                except Exception as e:
                    self.errors.append({
                        "type": "directory",
                        "message": f"无法创建{dir_name}: {dir_path}",
                        "detail": str(e)
                    })
            else:
                self.info.append({
                    "type": "directory",
                    "message": f"{dir_name}存在: {dir_path}"
                })
    
    def _check_docs_folder(self) -> None:
        """检查文档文件夹"""
        docs_folder = APP_CONFIG["docs_folder"]
        
        if not os.path.exists(docs_folder):
            self.warnings.append({
                "type": "docs_folder",
                "message": f"文档文件夹不存在: {docs_folder}",
                "solution": f"请创建文档文件夹并放入Word文档(.docx)文件"
            })
        else:
            # 检查文档文件数量
            try:
                files = os.listdir(docs_folder)
                doc_files = [f for f in files if (f.endswith('.docx') or f.endswith('.doc')) and not f.startswith('~$')]
                
                if not doc_files:
                    self.warnings.append({
                        "type": "docs_content",
                        "message": f"文档文件夹中没有找到Word文档: {docs_folder}",
                        "solution": "请在文档文件夹中放入.docx或.doc格式的Word文档"
                    })
                else:
                    self.info.append({
                        "type": "docs_content",
                        "message": f"找到 {len(doc_files)} 个Word文档文件（支持.docx/.doc）"
                    })
            except Exception as e:
                self.errors.append({
                    "type": "docs_folder",
                    "message": f"无法读取文档文件夹: {docs_folder}",
                    "detail": str(e)
                })
    
    def _check_port(self) -> None:
        """检查端口可用性"""
        import socket
        
        host = APP_CONFIG["host"]
        port = APP_CONFIG["port"]
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                self.info.append({
                    "type": "port",
                    "message": f"端口 {port} 可用"
                })
        except OSError:
            self.warnings.append({
                "type": "port",
                "message": f"端口 {port} 可能已被占用",
                "solution": "如果启动失败，请检查端口占用情况或修改配置文件中的端口号"
            })
    
    def print_results(self, result: Dict) -> None:
        """
        打印检查结果
        
        Args:
            result: 检查结果字典
        """
        print("\n" + "="*60)
        print("环境检查结果")
        print("="*60)
        
        if result["passed"]:
            print("✅ 环境检查通过")
        else:
            print("❌ 环境检查未通过")
        
        # 打印错误信息
        if result["errors"]:
            print("\n🚨 错误:")
            for i, error in enumerate(result["errors"], 1):
                print(f"  {i}. {error['message']}")
                if 'solution' in error:
                    if isinstance(error['solution'], list):
                        for solution in error['solution']:
                            print(f"     解决方案: {solution}")
                    else:
                        print(f"     解决方案: {error['solution']}")
                if 'detail' in error:
                    print(f"     详细: {error['detail']}")
        
        # 打印警告信息
        if result["warnings"]:
            print("\n⚠️ 警告:")
            for i, warning in enumerate(result["warnings"], 1):
                print(f"  {i}. {warning['message']}")
                if 'solution' in warning:
                    print(f"     建议: {warning['solution']}")
        
        # 打印信息
        if result["info"]:
            print("\nℹ️ 信息:")
            for i, info in enumerate(result["info"], 1):
                print(f"  {i}. {info['message']}")
        
        print("="*60)
        
        if result["passed"]:
            print(f"✅ 所有检查通过，可以启动服务器")
            print(f"🌐 访问地址: http://localhost:{APP_CONFIG['port']}")
        else:
            print("❌ 请解决上述错误后重新运行")
        print("="*60 + "\n")
    
    def get_startup_info(self) -> Dict:
        """
        获取启动信息
        
        Returns:
            Dict: 启动信息
        """
        return {
            "title": APP_CONFIG["title"],
            "host": APP_CONFIG["host"],
            "port": APP_CONFIG["port"],
            "docs_folder": APP_CONFIG["docs_folder"],
            "url": f"http://localhost:{APP_CONFIG['port']}"
        } 