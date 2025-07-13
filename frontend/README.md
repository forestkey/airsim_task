# AirSim 无人机控制系统前端

基于 Next.js 和 TypeScript 的无人机控制界面。

## 功能特性

- 实时飞行控制（起飞、降落、移动、悬停）
- 实时状态监控（位置、姿态、速度、电池）
- WebSocket 实时数据更新
- 响应式设计，支持移动端
- 现代化UI界面

## 技术栈

- Next.js 14
- TypeScript
- Tailwind CSS
- Socket.io Client
- Recharts
- Lucide Icons

## 快速开始

1. 安装依赖：
```bash
npm install
# 或
yarn install
```

2. 配置环境变量（可选）：
创建 `.env.local` 文件：
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

3. 启动开发服务器：
```bash
npm run dev
# 或
yarn dev
```

4. 访问 http://localhost:3000

## 项目结构

```
frontend/
├── app/              # Next.js App Router
│   ├── layout.tsx    # 根布局
│   ├── page.tsx      # 主页面
│   └── globals.css   # 全局样式
├── components/       # React组件
│   ├── ui/          # 通用UI组件
│   └── drone/       # 无人机相关组件
├── lib/             # 工具库
│   ├── api/         # API客户端
│   └── hooks/       # 自定义Hooks
├── types/           # TypeScript类型定义
└── public/          # 静态资源
```

## 主要组件

### ControlPanel
飞行控制面板，包含：
- 起飞/降落按钮
- 方向控制（八方向）
- 高度调整
- 速度控制
- 紧急停止

### StatusDisplay
状态显示面板，显示：
- 连接状态
- 位置信息（X, Y, Z）
- 姿态信息（Roll, Pitch, Yaw）
- 速度信息
- 飞行状态
- 电池电量
- GPS信息

## 构建部署

构建生产版本：
```bash
npm run build
# 或
yarn build
```

启动生产服务器：
```bash
npm start
# 或
yarn start
```

## 注意事项

1. 确保后端服务已启动
2. 确保 AirSim 仿真器已运行
3. WebSocket 连接会自动重连
4. 所有控制命令都有安全检查 