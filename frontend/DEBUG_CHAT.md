# 聊天界面调试指南

## 问题诊断

### 1. 打开浏览器控制台
按F12打开开发者工具，查看Console标签

### 2. 检查WebSocket连接
在控制台中应该看到：
- "Chat WebSocket connected"
- 没有WebSocket错误

### 3. 发送测试消息
发送一条消息"测试"，观察：
- 控制台是否有错误
- Network标签中是否有重复请求
- 消息列表的更新

### 4. 临时调试代码
如果用户消息仍然消失，可以在ChatInterface.tsx中添加调试日志：

```javascript
// 在handleSendMessage函数开始处添加
console.log('Sending message:', content)
console.log('Current messages before:', messages)

// 在setMessages后添加
setMessages(prev => {
  const newMessages = [...prev, userMessage]
  console.log('New messages:', newMessages)
  return newMessages
})
```

### 5. 检查状态管理
确认：
- `messages` 状态是否正确更新
- 组件是否意外重新挂载
- WebSocket回调是否正确处理

## 快速修复尝试

### 1. 强制刷新
```
Ctrl + F5
```

### 2. 清除localStorage
在控制台执行：
```javascript
localStorage.clear()
sessionStorage.clear()
```

### 3. 禁用WebSocket（临时）
修改ChatInterface.tsx，强制使用HTTP：
```javascript
if (false && chatService.isWebSocketConnected()) {
  // 暂时禁用WebSocket
}
```

## 预期行为验证
1. 发送消息后，用户消息立即显示
2. AI回复只显示一次
3. 消息列表按时间顺序排列
4. 输入框清空 