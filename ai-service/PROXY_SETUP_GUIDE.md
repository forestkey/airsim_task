# 代理设置指南

## 为什么需要代理？
如果Cherry Studio能正常访问Gemini但我们的服务不能，通常是因为Cherry Studio使用了系统代理或VPN。

## 快速设置步骤

### 1. 查找Cherry Studio的代理设置
Cherry Studio可能使用了以下方式之一：
- 系统代理
- 内置代理设置
- VPN连接

### 2. 获取代理地址
常见的代理格式：
- `http://127.0.0.1:7890`  (Clash默认端口)
- `http://127.0.0.1:1080`  (其他代理工具)
- `http://用户名:密码@代理地址:端口`

### 3. 在AI服务中配置代理

#### 方法1：在 .env 文件中添加（推荐）
编辑 `ai-service/.env` 文件，添加：
```
# 代理设置
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890

# 如果使用不同的模型
GEMINI_MODEL=gemini-1.5-flash
```

#### 方法2：在启动命令中设置
```bash
# Windows CMD
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Windows PowerShell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. 测试连接
运行测试脚本验证配置：
```bash
cd ai-service
python test_connections.py
```

## 常见代理工具端口

| 代理工具 | 默认HTTP端口 | 默认SOCKS端口 |
|---------|------------|--------------|
| Clash   | 7890       | 7891         |
| V2Ray   | 1080       | 1080         |
| Shadowsocks | 1080   | 1080         |
| 系统代理 | 查看系统设置 | -           |

## 查找系统代理设置

### Windows 10/11
1. 打开"设置" → "网络和Internet" → "代理"
2. 查看"手动设置代理"部分
3. 记录代理服务器地址和端口

### 通过命令行查看
```bash
# Windows
netsh winhttp show proxy

# 或查看环境变量
echo %HTTP_PROXY%
echo %HTTPS_PROXY%
```

## 故障排除

### 1. 仍然超时
- 确认代理服务正在运行
- 检查代理端口是否正确
- 尝试在浏览器中通过代理访问 https://generativelanguage.googleapis.com

### 2. 认证失败
如果代理需要认证，使用格式：
```
HTTP_PROXY=http://username:password@proxy-server:port
```

### 3. SSL证书错误
某些企业代理可能需要额外的证书配置。

## 备用方案
如果代理配置困难，系统会自动使用备用聊天服务，提供基本的无人机控制功能。 