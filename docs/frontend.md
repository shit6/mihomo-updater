# Mihomo自动更新服务 - 前端开发指南

本文档提供Mihomo自动更新服务前端项目的开发指南，适用于想要参与前端开发或定制前端界面的开发者。

## 技术栈

前端项目使用以下技术：

- **框架**: Vue 3 + TypeScript
- **UI库**: Naive UI
- **构建工具**: Vite
- **状态管理**: Vue 3 Composition API + Provide/Inject
- **CSS预处理器**: Less
- **HTTP客户端**: Axios
- **图标**: Iconify + @vicons/ionicons5
- **国际化**: vue-i18n

## 目录结构

```
frontend/
├── public/                 # 静态资源
├── src/                    # 源代码
│   ├── api/                # API请求封装
│   ├── assets/             # 静态资源
│   ├── components/         # 公共组件
│   ├── composables/        # 组合式函数
│   ├── config/             # 配置文件
│   ├── layouts/            # 布局组件
│   ├── router/             # 路由定义
│   ├── store/              # 状态管理
│   ├── styles/             # 全局样式
│   ├── types/              # TypeScript类型定义
│   ├── utils/              # 工具函数
│   ├── views/              # 页面组件
│   ├── App.vue             # 根组件
│   ├── main.ts             # 入口文件
│   └── shims-vue.d.ts      # Vue类型声明
├── .eslintrc.js            # ESLint配置
├── .prettierrc             # Prettier配置
├── index.html              # HTML模板
├── package.json            # 依赖配置
├── tsconfig.json           # TypeScript配置
└── vite.config.ts          # Vite配置
```

## 环境准备

### 开发环境要求

- Node.js 16.x 以上
- npm 7.x 以上或 yarn 1.22.x 以上

### 依赖安装

本项目使用严格的依赖版本锁定。请使用以下命令安装依赖：

```bash
# 安装所有锁定的依赖
npm ci
```

如果你是第一次安装，没有`package-lock.json`文件，请使用：

```bash
npm install
```

## 开发服务器

### 标准开发模式

```bash
# 启动开发服务器（支持热重载）
npm run dev
```

### 面向远程开发的模式

如果需要在远程服务器上开发，并从其他设备访问：

```bash
# 启动支持远程访问的开发服务器
npm run dev:host
```

### 调试模式

使用调试模式可以在命令行中看到更多错误信息：

```bash
# 启动带调试功能的开发服务器
npm run dev:debug
```

### 强制清除缓存模式

如果遇到缓存问题（特别是在TypeScript文件上），可以使用：

```bash
# 强制清除缓存并启动开发服务器
npm run dev:force
```

## 构建生产版本

```bash
# 类型检查
npm run type-check

# 构建生产版本
npm run build

# 预览生产构建（支持远程访问）
npm run preview
```

## 代码规范和质量

```bash
# 运行代码检查
npm run lint

# 运行代码检查并自动修复
npm run lint:fix

# 运行类型检查
npm run type-check
```

## 远程开发与调试

本项目支持远程开发和调试，适合在服务器上开发时使用：

### 远程开发流程

1. 在远程服务器上启动开发服务器：
   ```bash
   npm run dev:host
   ```

2. 在本地浏览器中访问：
   ```
   http://远程服务器IP:3000
   ```

### VSCode调试配置

项目已配置VSCode调试。在`.vscode/launch.json`中提供了以下配置：

- **对本地启动Chrome调试**：启动Chrome调试本地开发服务器
- **对远程地址启动Chrome调试**：启动Chrome调试远程开发服务器

使用方法：
1. 先运行开发服务器：`npm run dev`或`npm run dev:host`
2. 在VSCode中按F5或点击"运行和调试"按钮
3. 选择相应的调试配置

## 代码结构说明

### 页面组件

页面组件位于`src/views/`目录，主要包括：

- **Dashboard.vue**: 主仪表盘页面
- **Config.vue**: 配置管理页面
- **LogView.vue**: 日志查看页面
- **UpdateHistory.vue**: 更新历史页面

### API调用

API请求封装在`src/api/`目录中：

- **config.ts**: 配置相关API
- **update.ts**: 更新相关API
- **log.ts**: 日志相关API

示例用法：

```typescript
import { getConfig, updateConfig } from '@/api/config';

// 获取配置
const config = await getConfig();

// 更新配置
await updateConfig({ fetch_url: 'https://example.com/config.yaml' });
```

### 状态管理

项目使用Vue 3 Composition API进行状态管理，主要在`src/store/`目录：

- **config.ts**: 配置状态
- **update.ts**: 更新状态
- **theme.ts**: 主题状态

## 主题定制

项目使用Naive UI的主题系统，可以在`src/config/theme.ts`中修改主题配置：

```typescript
// 修改主题色
const themeOverrides = {
  common: {
    primaryColor: '#3366FF',
    primaryColorHover: '#5C85FF',
    // 其他颜色...
  }
};
```

## 国际化支持

项目使用vue-i18n实现国际化，语言文件位于`src/locales/`目录。

添加新语言支持：

1. 创建新的语言文件，如`src/locales/fr.ts`
2. 在`src/config/i18n.ts`中导入并注册

## 常见问题解决

### 找不到模块错误

如果遇到"找不到模块"错误，尝试：

```bash
# 清除node_modules并重新安装
rm -rf node_modules
npm ci
```

### 类型错误

TypeScript类型错误通常在开发过程中就会显示。要单独检查类型问题：

```bash
npm run type-check
```

### 编译缓存问题

如果修改没有生效，可能是Vite缓存问题：

```bash
# 强制清除缓存并重启
npm run dev:force
```

### 热重载不工作

如果热重载不工作，可以尝试：

1. 检查浏览器控制台是否有错误
2. 关闭并重启开发服务器
3. 清除浏览器缓存

## 贡献指南

1. Fork 仓库并克隆到本地
2. 创建新分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature-name`
5. 提交Pull Request

请确保你的代码：
- 通过所有的lint检查：`npm run lint`
- 通过所有的类型检查：`npm run type-check`
- 有必要的测试和文档 