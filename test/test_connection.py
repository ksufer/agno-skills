"""
DashScope 连接测试脚本

用于验证 DASHSCOPE_API_KEY 是否正确配置。
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

def test_api_key():
    """测试 API 密钥配置"""
    print("=" * 60)
    print("DashScope API 连接测试")
    print("=" * 60)
    print()
    
    # 检查 API 密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    
    if not api_key:
        print("❌ DASHSCOPE_API_KEY 未设置")
        print()
        print("请设置环境变量：")
        print()
        print("方法 1 - 使用 .env 文件（推荐）：")
        print("  在项目根目录创建 .env 文件，添加：")
        print("  DASHSCOPE_API_KEY=sk-your-api-key")
        print()
        print("方法 2 - PowerShell：")
        print('  $env:DASHSCOPE_API_KEY="sk-your-api-key"')
        print()
        print("方法 3 - CMD：")
        print("  set DASHSCOPE_API_KEY=sk-your-api-key")
        print()
        print("获取 API 密钥：https://dashscope.console.aliyun.com/")
        return False
    
    print(f"✅ API 密钥已设置")
    print(f"   前 10 位: {api_key[:10]}...")
    print(f"   长度: {len(api_key)} 字符")
    print()
    
    # 测试连接
    print("正在测试 DashScope 连接...")
    print()
    
    try:
        from agno.agent import Agent
        from agno.models.dashscope import DashScope
        
        agent = Agent(
            model=DashScope(
                id="qwen-plus",
                # 中国大陆用户必须使用此端点
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            ),
            markdown=True
        )
        
        response = agent.run("你好，请用一句话介绍你自己")
        
        print("✅ DashScope 连接成功！")
        print()
        print("模型响应：")
        print("-" * 60)
        print(response.content)
        print("-" * 60)
        print()
        print("🎉 配置完成！现在可以运行示例了：")
        print("   python examples/basic_usage.py")
        return True
        
    except Exception as e:
        print(f"❌ 连接失败")
        print()
        print(f"错误信息: {str(e)}")
        print()
        
        # 提供诊断信息
        error_msg = str(e).lower()
        
        if "401" in error_msg or "invalid" in error_msg or "incorrect" in error_msg:
            print("诊断：API 密钥无效")
            print()
            print("请检查：")
            print("  1. API 密钥是否正确复制（包括 sk- 前缀）")
            print("  2. 密钥是否已启用")
            print("  3. 访问 https://dashscope.console.aliyun.com/ 验证密钥")
        
        elif "network" in error_msg or "connection" in error_msg:
            print("诊断：网络连接问题")
            print()
            print("请检查：")
            print("  1. 网络连接是否正常")
            print("  2. 是否可以访问阿里云服务")
        
        else:
            print("诊断：未知错误")
            print()
            print("请查看：")
            print("  - docs/quick_start.md 获取详细帮助")
            print("  - docs/dashscope_migration.md 了解配置详情")
        
        return False


if __name__ == "__main__":
    success = test_api_key()
    exit(0 if success else 1)
