# AI服务故障排除指南

## 运行诊断测试
首先运行测试脚本来诊断问题：
```bash
cd ai-service
python test_client_with_proxy.py
```

## 常见问题和解决方案

### 1. Gemini API超时错误
**错误**: `Timeout of 60.0s exceeded, 503 failed to connect`

**原因**: 代理配置问题或网络限制

**解决方案**:

#### 方案A: 检查Cherry Studio的代理设置
1. 打开Cherry Studio的设置
2. 查看网络/代理配置
3. 记录代理地址和端口
4. 在 `.env` 文件中使用相同的代理：
   ```
   HTTP_PROXY=http://127.0.0.1:你的端口
   HTTPS_PROXY=http://127.0.0.1:你的端口
   ```

#### 方案B: 尝试不同的代理端口
常见端口：
- 7890 (Clash)
- 7897 (你当前使用的)
- 1080 (Shadowsocks/V2Ray)
- 10809 (V2RayN)

#### 方案C: 使用系统代理
```bash
# 查看Windows系统代理
netsh winhttp show proxy

# 或在PowerShell中
Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' | Select-Object ProxyServer, ProxyEnable
```

#### 方案D: 直接测试Gemini API
```python
# 创建test_direct.py
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'

import google.generativeai as genai
genai.configure(api_key='你的API密钥')
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content('Hello')
print(response.text)
```

### 2. MCP 401认证错误
**错误**: `401 Unauthorized for url 'http://localhost:8000/api/v1/mcp/execute'`

**原因**: 主后端服务未运行或认证token不匹配

**解决方案**:
1. 确保主后端服务正在运行：
   ```bash
   # 在另一个终端
   cd backend
   conda activate drone308  # 或你的环境名
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. 验证服务健康状态：
   ```bash
   curl http://localhost:8000/health
   ```

3. 检查认证token是否匹配：
   - AI服务: `ai-service/app/core/config.py` 中的 `MCP_AUTH_TOKEN`
   - 主后端: `backend/app/mcp/server.py` 中的 `expected_token`
   - 两者必须都是 `"default-dev-token"`

### 3. 使用备用聊天服务
如果Gemini API持续无法访问，系统会自动使用备用服务。

**支持的命令**:
```
起飞 / takeoff - 起飞到指定高度
降落 / land - 降落
前进 / forward - 向前飞行
后退 / backward - 向后飞行
左移 / left - 向左移动
右移 / right - 向右移动
上升 / up - 向上飞行
下降 / down - 向下飞行
悬停 / hover - 悬停
```

**示例**:
- "起飞到10米"
- "前进5米"
- "降落"

### 4. 环境变量完整配置
确保 `ai-service/.env` 包含：
```env
# Gemini配置
GEMINI_API_KEY=你的API密钥
GEMINI_MODEL=gemini-2.5-flash

# 代理配置（根据实际情况）
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897

# 服务配置
DRONE_SERVICE_URL=http://localhost:8000
MCP_AUTH_TOKEN=default-dev-token
```

### 5. 快速启动命令
```bash
# 终端1: 启动主后端
cd backend
conda activate drone308
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 终端2: 启动AI服务
cd ai-service
conda activate drone_312
set HTTP_PROXY=http://127.0.0.1:7897
set HTTPS_PROXY=http://127.0.0.1:7897
uvicorn app.main:app --host 0.0.0.0 --port 8001

# 终端3: 启动前端
cd frontend
npm run dev
```

### 6. 验证服务状态
1. 主后端: http://localhost:8000/docs
2. AI服务: http://localhost:8001/docs
3. 前端: http://localhost:3000

## 调试建议
1. 运行 `test_client_with_proxy.py` 查看详细诊断信息
2. 查看AI服务日志中的代理配置信息
3. 如果备用服务正常工作，说明主要问题是Gemini API访问
4. 考虑临时使用备用服务进行开发和测试 