# 贡献指南

感谢你考虑为Mihomo自动更新服务项目做出贡献！以下是参与本项目的指南。

## 行为准则

请保持尊重和专业，善待其他贡献者和用户。我们期望所有参与者遵守以下准则：

- 使用包容性语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注于对社区最有利的事情

## 如何贡献

### 报告Bug

如果你发现了Bug，请在GitHub issues中报告，并包含以下信息：

1. Bug简短明确的标题
2. 重现步骤
3. 预期行为
4. 实际行为
5. 环境信息（操作系统、Docker版本等）
6. 相关日志或截图

### 提交功能请求

如果你有新功能或改进建议，也请通过GitHub issues提交，并包含：

1. 清晰描述你希望的功能
2. 这个功能会解决什么问题
3. 可能的实现方案（如果你有想法）

### 贡献代码

1. Fork项目仓库
2. 创建你的特性分支：`git checkout -b feature/amazing-feature`
3. 提交你的更改：`git commit -m 'Add some amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 提交Pull Request

#### 代码风格

- **后端代码**：遵循PEP 8规范
- **前端代码**：遵循项目的ESLint和Prettier配置

#### Pull Request流程

1. 确保PR描述清晰地说明了更改内容和目的
2. 如果PR解决了某个issue，请在PR描述中使用关键词引用它（例如："Fixes #123"）
3. 确保所有自动化测试通过
4. 确保代码经过了适当的测试
5. 保持PR专注于单一问题或功能

## 开发环境设置

### 后端开发

1. 安装Python 3.6+
2. 克隆仓库：`git clone https://github.com/zztdandan/mihomo-updater.git`
3. 进入后端目录：`cd mihomo-updater/backend`
4. 安装依赖：`pip install -r requirements.txt`
5. 启动开发服务器：`python app.py`

### 前端开发

1. 安装Node.js 16+和npm
2. 进入前端目录：`cd mihomo-updater/frontend`
3. 安装依赖：`npm ci`
4. 启动开发服务器：`npm run dev`

详细前端开发指南请参阅[前端开发文档](frontend.md)。

## 版本控制和发布

我们使用[语义化版本](https://semver.org/)进行版本控制。版本格式为：MAJOR.MINOR.PATCH

- MAJOR：不兼容的API变更
- MINOR：向后兼容的功能新增
- PATCH：向后兼容的问题修复

## 文档

如果你修改了功能或添加了新功能，请同时更新相关文档。这包括：

- README.md中的功能说明
- docs/目录中的相关文档
- 代码注释

## 问题和疑问

如有任何问题，可以在GitHub Issues中提问，或联系项目维护者。 