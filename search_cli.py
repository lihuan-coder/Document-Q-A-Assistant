#!/usr/bin/env python3
"""
命令行文档搜索工具
智能文档问答助手的命令行版本

Author: AI Assistant
Version: 2.0.0
"""

import sys
from app.services import DocumentSearchService, KeywordExtractor
from app.utils import main_logger, EnvironmentChecker
from config import APP_CONFIG, SEARCH_CONFIG


def main():
    """命令行搜索主函数"""
    print("="*60)
    print("智能文档搜索工具 (智能文档问答助手命令行版)")
    print("="*60)
    
    # 环境检查
    env_checker = EnvironmentChecker()
    is_passed, result = env_checker.check_all()
    
    if not is_passed:
        print("❌ 环境检查未通过，请解决问题后重试")
        return
    
    # 初始化服务
    try:
        document_searcher = DocumentSearchService(
            folder_path=APP_CONFIG["docs_folder"],
            enhanced_context=SEARCH_CONFIG["enhanced_context"]
        )
        keyword_extractor = KeywordExtractor()
        print(f"✅ 服务初始化成功，文档文件夹: {APP_CONFIG['docs_folder']}")
        print(f"📊 上下文模式: {'增强模式' if SEARCH_CONFIG['enhanced_context'] else '标准模式'}")
    except Exception as e:
        print(f"❌ 服务初始化失败: {e}")
        return
    
    print("\n📝 使用说明:")
    print("1. 输入您的问题，系统会自动提取关键词进行搜索")
    print("2. 输入 'quit' 或 'exit' 退出程序")
    print("3. 输入 'clear' 清除搜索缓存")
    print("4. 输入 'status' 查看系统状态")
    print("-" * 60)
    
    while True:
        try:
            # 获取用户输入
            question = input("\n🤔 请输入您的问题: ").strip()
            
            if not question:
                print("⚠️ 问题不能为空，请重新输入")
                continue
            
            # 处理特殊命令
            if question.lower() in ['quit', 'exit']:
                print("👋 再见!")
                break
            elif question.lower() == 'clear':
                document_searcher.clear_cache()
                print("✅ 缓存已清除")
                continue
            elif question.lower() == 'status':
                cache_info = document_searcher.get_cache_info()
                print(f"📊 系统状态:")
                print(f"   - 缓存大小: {cache_info['cache_size']}")
                print(f"   - 最大缓存: {cache_info['max_cache_size']}")
                continue
            
            print(f"\n🔍 正在分析问题: {question}")
            
            # 提取关键词
            keywords = keyword_extractor.extract_keywords(question)
            print(f"🏷️ 提取的关键词: {', '.join(keywords) if keywords else '无'}")
            
            if not keywords:
                print("⚠️ 未能提取到有效关键词，请尝试更具体的问题")
                continue
            
            # 搜索文档
            print("📚 正在搜索文档...")
            search_results = document_searcher.search_documents(keywords)
            
            if not search_results:
                print("😅 抱歉，没有找到相关的文档内容")
                continue
            
            # 显示搜索结果
            print(f"\n📋 搜索结果 (共找到 {len(search_results)} 条):")
            print("-" * 60)
            
            for i, result in enumerate(search_results, 1):
                print(f"\n{i}. 📄 文件: {result['文件名']}")
                print(f"   📍 位置: 第 {result['文段起始段落号']} 段")
                print(f"   🏷️ 关键词: {', '.join(result['关键词'])}")
                
                if result.get('上下文'):
                    print(f"   📖 上下文: {result['上下文']}")
                
                # 显示内容预览（限制长度）
                content = result['内容']
                if len(content) > 200:
                    content = content[:200] + "..."
                print(f"   📝 内容: {content}")
                
                if i < len(search_results):
                    print("-" * 40)
            
            # 保存结果
            output_file = "search_results.json"
            document_searcher.save_results(output_file)
            print(f"\n💾 详细结果已保存到: {output_file}")
            
        except KeyboardInterrupt:
            print("\n👋 程序已退出")
            break
        except Exception as e:
            print(f"\n❌ 处理过程中发生错误: {e}")
            main_logger.error(f"命令行搜索错误: {e}")
            continue


if __name__ == "__main__":
    main() 