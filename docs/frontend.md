# Mihomo自动更新服务前端

这是Mihomo自动更新服务的前端项目，使用Vue 3、TypeScript和Naive UI构建。

## 安装依赖

本项目使用了严格的依赖版本锁定。请使用以下命令安装依赖：

```bash
# 安装所有锁定的依赖
npm run install:deps
```

如果你是第一次安装，没有`package-lock.json`文件，请使用：

```bash
npm install
```

## 开发

```bash
# 启动开发服务器（支持远程访问）
npm run dev

# 启动带调试功能的开发服务器
npm run dev:debug

# 强制清除缓存并启动开发服务器
npm run dev:force
```

## 远程开发

本项目支持远程开发和调试：

1. 在远程服务器上运行 `npm run dev`，这会启动一个监听所有网络接口的开发服务器
2. 在本地浏览器中访问 `http://远程服务器IP:3000`
3. 在VSCode中，可以使用"对远程地址启动Chrome调试"配置进行调试

## 调试

本项目已配置VSCode调试。要启动调试：

1. 先运行 `npm run dev`
2. 在VSCode中按F5或点击"运行和调试"按钮
3. 选择"对本地启动Chrome调试"或"对远程地址启动Chrome调试"配置

这将打开一个Chrome浏览器，你可以在VSCode中设置断点进行调试。

## 构建

```bash
# 类型检查
npm run type-check

# 构建生产版本
npm run build

# 预览生产构建（支持远程访问）
npm run preview
```

## 代码规范

```bash
# 运行代码检查和自动修复
npm run lint
```

## 常见问题解决

### 找不到文件错误

如果遇到找不到`main.js`等文件的错误，可能是因为项目已经迁移到TypeScript，但某些引用还指向JavaScript文件。解决方法：

1. 检查`index.html`中的脚本引用是否为`main.ts`而不是`main.js`
2. 运行`npm run dev:force`强制清除缓存并重新启动
3. 确保所有JS文件都已转换为TS文件 