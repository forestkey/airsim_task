# 使用调试版聊天界面

## 临时使用调试版本
为了诊断问题，可以临时使用带调试功能的ChatInterface：

### 1. 修改page.tsx
编辑 `frontend/app/page.tsx`，修改import语句：

```typescript
// 原来的
import ChatInterface from '@/src/components/ChatInterface/ChatInterface'

// 改为
import ChatInterface from '@/src/components/ChatInterface/ChatInterfaceDebug'
```

### 2. 重新加载页面
保存后，前端会自动重新编译。刷新浏览器页面。

### 3. 查看调试信息
调试版本会在聊天界面顶部显示一个灰色的调试面板，显示：
- 实时日志
- 消息计数
- 连接状态
- 加载状态

### 4. 测试并观察
1. 发送一条消息
2. 观察调试面板中的日志
3. 检查消息计数是否正确增加
4. 查看控制台是否有额外错误

### 5. 恢复正常版本
测试完成后，将import语句改回原来的即可。

## 调试信息说明
- `Component mounted`: 组件加载
- `WebSocket message received`: 收到WebSocket消息
- `Adding user message`: 添加用户消息
- `Using WebSocket to send`: 使用WebSocket发送
- `Adding AI message`: 添加AI回复
- `Messages: X`: 当前消息总数

通过这些信息可以诊断：
- 消息是否正确添加到列表
- WebSocket通信是否正常
- 组件状态是否正确更新 