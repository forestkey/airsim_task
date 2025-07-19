# 修复用户消息不显示的问题

## 已实施的修复

1. **改进状态更新方式**
   - 使用函数式setState确保使用最新状态
   - 添加调试日志追踪消息添加过程

2. **修复WebSocket连接**
   - 只在组件可见时连接WebSocket
   - 添加isVisible到useEffect依赖数组

3. **添加调试日志**
   ```javascript
   console.log('[ChatInterface] Adding user message:', content)
   console.log('[ChatInterface] Current messages before adding user:', prev.length)
   console.log('[ChatInterface] Messages after adding user:', newMessages.length)
   console.log('[ChatInterface] Adding AI reply, current messages:', prevMessages.length)
   ```

## 测试步骤

1. **刷新页面**
   - 强制刷新：Ctrl + F5
   - 打开浏览器控制台（F12）

2. **发送测试消息**
   - 点击右下角的AI助手按钮打开聊天界面
   - 发送"你好"
   - 观察控制台日志

3. **预期看到的日志**
   ```
   [ChatInterface] Adding user message: 你好
   [ChatInterface] Current messages before adding user: 0
   [ChatInterface] Messages after adding user: 1
   [ChatInterface] Adding AI reply, current messages: 1
   ```

## 如果问题仍然存在

### 可能的原因
1. 组件重新渲染导致状态丢失
2. WebSocket回调闭包问题
3. React严格模式导致的双重渲染

### 进一步调试
1. 在MessageList组件中添加日志：
   ```javascript
   console.log('[MessageList] Rendering messages:', messages.length, messages)
   ```

2. 检查是否有其他地方清空了messages

3. 禁用React严格模式（临时）：
   在 `frontend/app/layout.tsx` 中移除 `<React.StrictMode>`

## 临时解决方案

如果上述修复都不起作用，可以使用以下临时方案：

### 方案1：使用localStorage保存消息
```javascript
// 保存消息到localStorage
useEffect(() => {
  localStorage.setItem('chat-messages', JSON.stringify(messages))
}, [messages])

// 从localStorage恢复消息
useEffect(() => {
  const saved = localStorage.getItem('chat-messages')
  if (saved) {
    setMessages(JSON.parse(saved))
  }
}, [])
```

### 方案2：使用useReducer替代useState
使用useReducer可以避免一些闭包问题。

## 验证修复效果

1. 用户消息应该立即显示在聊天界面
2. AI回复应该显示在用户消息下方
3. 消息列表应该保持完整的对话历史
4. 刷新页面后消息会清空（这是正常的） 