# 修复 AI 助手连接问题

## 问题描述
AI 助手显示"连接中..."，输入框被禁用，无法发送消息。

## 原因
WebSocket 连接逻辑需要后端发送 'connected' 类型的消息来确认连接成功。

## 临时解决方案

### 方案1：修改前端代码（临时）
在 `frontend/src/components/ChatInterface/ChatInterface.tsx` 中，可以暂时改回之前的逻辑：

```typescript
// 在 useEffect 中，WebSocket 连接后立即设置连接状态
setIsConnected(true)  // 在 connectWebSocket 调用后添加这行
```

### 方案2：更新后端代码（推荐）
确保后端在 WebSocket 连接建立时发送连接确认消息：

```python
# 在后端的 WebSocket 处理代码中
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    # 发送连接成功消息
    await websocket.send_json({
        "type": "connected",
        "data": {"message": "WebSocket connected successfully"}
    })
```

## 界面改进
已将 AI 助手从底部改为右侧悬浮窗：
- 最小化时：显示在右侧中央，垂直显示"AI 助手"文字
- 展开时：固定在右侧，高度 600px，宽度 396px
- 添加了平滑的过渡动画效果

## 使用说明
1. 确保后端服务正在运行
2. 刷新前端页面
3. AI 助手会自动出现在右侧
4. 点击最小化按钮可以收起对话框
5. 点击展开按钮重新打开对话框 