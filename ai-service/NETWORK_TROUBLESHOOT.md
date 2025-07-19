# 网络连接问题排查指南

## 问题描述
遇到以下错误：
- `Timeout of 60.0s exceeded`
- `503 failed to connect to all addresses`
- 无法连接到Google服务器 (142.250.196.202:443)

## 原因分析
1. **网络防火墙**：可能阻止了对Google API的访问
2. **代理设置**：企业网络可能需要代理
3. **DNS问题**：无法解析Google服务器地址
4. **地区限制**：某些地区可能无法直接访问Google服务

## 解决方案

### 方案1：使用备用聊天服务（已实现）
系统已自动切换到备用聊天服务，提供基本的无人机控制功能：
- 支持命令：起飞、降落、前进、后退、左移、右移、上升、下降
- 示例："起飞到10米"、"前进5米"、"降落"

### 方案2：配置代理（如果有）
```python
# 在 ai-service/.env 文件中添加
HTTP_PROXY=http://your-proxy:port
HTTPS_PROXY=http://your-proxy:port
```

### 方案3：使用VPN
如果在受限网络环境，考虑使用VPN连接。

### 方案4：检查防火墙
```bash
# Windows检查防火墙
netsh advfirewall show allprofiles

# 测试连接
curl https://generativelanguage.googleapis.com/v1beta/models
```

### 方案5：更换API服务
考虑使用其他AI服务：
- OpenAI API
- 百度文心一言
- 阿里通义千问

## 备用聊天功能说明
当Gemini API不可用时，系统会自动使用备用聊天服务：

**支持的命令**：
- 起飞：`起飞`、`takeoff`、`飞起来`
- 降落：`降落`、`land`、`着陆`
- 前进：`前进`、`forward`、`向前`
- 后退：`后退`、`backward`、`向后`
- 左移：`左移`、`left`、`向左`
- 右移：`右移`、`right`、`向右`
- 上升：`上升`、`up`、`向上`
- 下降：`下降`、`down`、`向下`
- 悬停：`悬停`、`hover`、`停`

**使用示例**：
- "起飞到20米"
- "前进10米"
- "向左移动5米"
- "降落"

## 验证步骤
1. 重启AI服务
2. 在聊天窗口输入"你好"
3. 如果回复正常，说明备用服务工作正常
4. 尝试控制命令如"起飞" 