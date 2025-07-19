#!/usr/bin/env python
"""
测试脚本 - 验证 Gemini API 配置
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import google.generativeai as genai
    print("✓ google-generativeai 包已安装")
except ImportError:
    print("✗ google-generativeai 包未安装")
    print("请运行: pip install google-generativeai")
    sys.exit(1)

# Test API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("✗ GEMINI_API_KEY 未设置")
    print("请在 .env 文件中设置 GEMINI_API_KEY")
    sys.exit(1)
else:
    print(f"✓ GEMINI_API_KEY 已设置 (长度: {len(api_key)})")

# Test basic Gemini connection
print("\n测试 Gemini API 连接...")
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello, this is a test. Reply with 'Test successful!'")
    print(f"✓ API 连接成功")
    print(f"响应: {response.text[:100]}...")
except Exception as e:
    print(f"✗ API 连接失败: {e}")
    sys.exit(1)

# Test our client
print("\n测试 Gemini 客户端...")
try:
    from app.core.config import settings
    from app.gemini.client import gemini_client
    
    async def test_client():
        response = await gemini_client.simple_chat("你好，这是一个测试。请回复'测试成功！'")
        print(f"✓ 客户端测试成功")
        print(f"响应: {response[:100]}...")
    
    asyncio.run(test_client())
except Exception as e:
    print(f"✗ 客户端测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n所有测试完成！") 