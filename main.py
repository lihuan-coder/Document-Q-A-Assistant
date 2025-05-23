#!/usr/bin/env python3
"""
智能文档问答助手 - 主程序入口
基于千问大模型的智能文档搜索和问答应用

Author: AI Assistant
Version: 2.0.0
"""

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.web import QAService
from app.utils import EnvironmentChecker, main_logger
from config import APP_CONFIG


# 创建FastAPI应用实例
app = FastAPI(
    title=APP_CONFIG["title"],
    description="基于千问大模型的智能文档搜索和问答应用",
    version="2.0.0"
)

# 初始化服务
qa_service = QAService()

# 配置模板和静态文件
templates = Jinja2Templates(directory=APP_CONFIG["templates_dir"])
app.mount("/static", StaticFiles(directory=APP_CONFIG["static_dir"]), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    渲染主页
    
    Args:
        request: FastAPI请求对象
        
    Returns:
        HTMLResponse: 主页HTML响应
    """
    main_logger.info("访问主页")
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.websocket("/ws/ask")
async def websocket_ask(websocket: WebSocket):
    """
    WebSocket问答接口
    处理用户问题并实时返回答案
    
    Args:
        websocket: WebSocket连接对象
    """
    await qa_service.ws_manager.connect(websocket)
    
    try:
        # 接收用户问题
        data = await websocket.receive_json()
        question = data.get("question", "").strip()
        
        if not question:
            await qa_service.ws_manager.send_json(websocket, {
                "step": "error",
                "message": "问题不能为空"
            })
            return
        
        main_logger.info(f"收到用户问题: {question}")
        
        # 处理问题
        await qa_service.process_question(websocket, question)
        
    except WebSocketDisconnect:
        main_logger.info("WebSocket连接断开")
        qa_service.ws_manager.disconnect(websocket)
    except Exception as e:
        main_logger.error(f"WebSocket处理错误: {e}")
        try:
            await qa_service.ws_manager.send_json(websocket, {
                "step": "error", 
                "message": f"处理请求时发生错误: {str(e)}"
            })
        except:
            pass
    finally:
        # 确保连接关闭
        try:
            await websocket.close()
        except:
            pass


@app.get("/api/status")
async def get_status():
    """
    获取系统状态信息
    
    Returns:
        dict: 系统状态信息
    """
    return qa_service.get_service_status()


@app.post("/api/clear-cache")
async def clear_cache():
    """
    清除系统缓存
    
    Returns:
        dict: 操作结果
    """
    try:
        qa_service.clear_caches()
        main_logger.info("缓存已清除")
        return {"success": True, "message": "缓存已清除"}
    except Exception as e:
        main_logger.error(f"清除缓存失败: {e}")
        return {"success": False, "message": f"清除缓存失败: {str(e)}"}


def main():
    """主函数，启动应用"""
    print("正在启动智能文档问答助手...")
    
    # 环境检查
    env_checker = EnvironmentChecker()
    is_passed, result = env_checker.check_all()
    env_checker.print_results(result)
    
    if not is_passed:
        return
    
    # 启动服务器
    main_logger.info("正在启动服务器...")
    print(f"\n🚀 启动服务器...")
    print(f"📖 应用名称: {APP_CONFIG['title']}")
    print(f"🌐 访问地址: http://localhost:{APP_CONFIG['port']}")
    print(f"📁 文档文件夹: {APP_CONFIG['docs_folder']}")
    print(f"🔄 按 Ctrl+C 停止服务器\n")
    
    try:
        uvicorn.run(
            app,
            host=APP_CONFIG["host"],
            port=APP_CONFIG["port"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        main_logger.info("服务器已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")
        main_logger.error(f"服务器启动失败: {e}")


if __name__ == "__main__":
    main() 