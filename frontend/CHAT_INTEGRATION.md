# 前端聊天功能集成说明

## 集成步骤

### 1. 在主页面中添加聊天组件

编辑您的主页面组件（例如 `app/page.tsx` 或 `pages/index.tsx`）：

```tsx
import { ChatInterface } from '@/components/ChatInterface/ChatInterface'

export default function HomePage() {
  return (
    <div>
      {/* 您现有的页面内容 */}
      
      {/* 添加聊天界面 */}
      <ChatInterface />
    </div>
  )
}
```

### 2. 处理路径别名问题

如果遇到 `@/` 路径别名无法解析的问题，有两个解决方案：

**方案 A：配置 TypeScript 路径映射**

在 `tsconfig.json` 中添加：
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

**方案 B：使用相对路径**

将所有 `@/` 导入改为相对路径：
- `@/services/chatService` → `../../services/chatService`
- `@/config/services` → `../../config/services`

### 3. 移动服务文件到正确位置

如果您的项目结构不同，需要调整文件位置：

```bash
# 如果 services 目录不在 src 下
mkdir -p src/services
mv frontend/src/services/chatService.ts src/services/

# 如果 config 目录不在 src 下
mkdir -p src/config  
mv frontend/src/config/services.ts src/config/
```

### 4. 修复 Button 组件兼容性

聊天组件使用了一些 Button 的属性，如果与您现有的 Button 组件不兼容，创建一个包装器：

```tsx
// components/ChatInterface/ChatButton.tsx
import { Button as BaseButton } from '../ui/Button'

interface ChatButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'icon'
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  className?: string
  title?: string
}

export const ChatButton: React.FC<ChatButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  ...props
}) => {
  // 映射 variant
  const buttonVariant = variant === 'ghost' ? 'secondary' : variant
  
  // 映射 size
  const buttonSize = size === 'icon' ? 'sm' : size
  
  return (
    <BaseButton 
      variant={buttonVariant} 
      size={buttonSize}
      {...props}
    >
      {children}
    </BaseButton>
  )
}
```

然后在聊天组件中使用 `ChatButton` 替代 `Button`。

### 5. 环境变量配置

在 `.env.local` 中添加：
```
NEXT_PUBLIC_AI_API=http://localhost:8001
NEXT_PUBLIC_WS_CHAT=ws://localhost:8001
```

## 样式调整

### 位置调整

如果需要调整聊天窗口位置，修改 `ChatInterface.tsx`：

```tsx
// 左下角
<div className="fixed bottom-4 left-4 ...">

// 右上角
<div className="fixed top-4 right-4 ...">

// 居中底部
<div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 ...">
```

### 尺寸调整

```tsx
// 更大的窗口
<div className="... w-[500px] h-[700px] ...">

// 响应式尺寸
<div className="... w-full max-w-md h-[600px] md:w-96 ...">
```

### 主题适配

如果使用暗色主题：

```tsx
<div className="... bg-gray-800 text-white ...">
  {/* 调整内部组件的颜色类名 */}
</div>
```

## 功能扩展

### 1. 添加语音输入

```tsx
const handleVoiceInput = () => {
  const recognition = new webkitSpeechRecognition()
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript
    handleSendMessage(transcript)
  }
  recognition.start()
}
```

### 2. 添加预设命令

```tsx
const presetCommands = [
  { label: '起飞', command: '起飞到10米' },
  { label: '降落', command: '降落' },
  { label: '查看状态', command: '查看无人机状态' },
]

// 在界面中添加快捷按钮
{presetCommands.map(cmd => (
  <button onClick={() => handleSendMessage(cmd.command)}>
    {cmd.label}
  </button>
))}
```

### 3. 添加执行历史

```tsx
const [commandHistory, setCommandHistory] = useState<string[]>([])

// 保存成功执行的命令
const saveToHistory = (command: string) => {
  setCommandHistory(prev => [...prev, command].slice(-10))
}
```

## 故障排除

### WebSocket 连接失败
- 检查 AI 服务是否运行在 8001 端口
- 检查 CORS 配置
- 查看浏览器控制台网络错误

### 类型错误
- 确保安装了必要的类型定义：`npm install --save-dev @types/node`
- 检查 TypeScript 版本兼容性

### 样式冲突
- 使用 CSS Modules 或 styled-components 隔离样式
- 添加特定的类名前缀避免冲突 