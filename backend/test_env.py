#!/usr/bin/env python
"""
测试脚本 - 验证 drone_308 环境配置
"""

import sys
import importlib

def test_environment():
    """测试环境和依赖包"""
    print(f"Python 版本: {sys.version}")
    print(f"Python 路径: {sys.executable}\n")
    
    # 测试必要的包
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("airsim", "AirSim"),
        ("websockets", "WebSockets"),
        ("pydantic", "Pydantic"),
        ("numpy", "NumPy"),
    ]
    
    all_ok = True
    
    for package_name, display_name in required_packages:
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, "__version__", "版本未知")
            print(f"✓ {display_name}: {version}")
        except ImportError:
            print(f"✗ {display_name}: 未安装")
            all_ok = False
    
    print("\n" + "="*50)
    
    if all_ok:
        print("✓ 所有必要的包都已安装！")
        print("\n可以运行以下命令启动服务：")
        print("  uvicorn app.main:app --reload")
    else:
        print("✗ 某些包未安装，请检查 requirements.txt")
        print("\n运行以下命令安装缺失的包：")
        print("  pip install -r requirements.txt")
    
    return all_ok

if __name__ == "__main__":
    print("=== AirSim Drone Control 环境测试 ===\n")
    test_environment() 