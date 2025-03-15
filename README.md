# Mihomo自动更新服务

<p align="center">
  <img src="docs/images/logo.svg" width="150" />
</p>

<p align="center">
  一个用于自动更新Mihomo（Clash.Meta）配置文件和GeoIP数据的服务，具有美观的Web界面管理。
</p>

## 📝 项目简介

Mihomo自动更新服务是一个专为Mihomo（原Clash.Meta）用户设计的自动化工具，可以帮助用户自动更新订阅配置和地理位置数据，并提供美观的Web界面进行管理。

### 主要功能

- ✅ 自动定期从指定URL拉取最新的Clash配置文件
- ✅ 智能合并配置文件，只更新`proxies`、`proxy-groups`、`rules`部分
- ✅ 自动备份原配置文件，定期更新GeoIP数据
- ✅ 提供美观的响应式Web界面，支持一键跳转到Yacd面板

## 🖼️ 界面预览

<p align="center">
  <img src="docs/images/dashboard.png" width="80%" />
</p>

## 🚀 快速开始

### Docker部署（推荐）

```bash
# 克隆仓库
git clone https://github.com/zztdandan/mihomo-updater.git
cd mihomo-updater

# 构建镜像
docker-compose -f build/docker-compose.build.yml build

# 启动服务
docker-compose -f build/docker-compose.yml up -d
```

### 访问界面

- Web管理界面: `http://your-server-ip:3000`
- Yacd控制面板: `http://your-server-ip:8080`

## 📖 详细文档

- [详细安装和使用指南](docs/detailed-guide.md)
- [Docker部署指南](docs/docker-guide.md)
- [前端开发文档](docs/frontend.md)

## 🧰 项目结构

```
mihomo-updater/
├── frontend/             # 前端Vue代码
├── backend/              # 后端Python代码
├── build/                # 打包与部署配置
├── data/                 # 数据存储目录
└── docs/                 # 详细文档
```

## 🔧 技术栈

- 前端：Vue 3 + TypeScript + Naive UI
- 后端：Python + Flask
- 部署：Docker + Docker Compose

## 📄 许可证

MIT

## 🤝 贡献

欢迎提交问题和贡献代码！请查看[贡献指南](docs/contributing.md)。

## 📣 致谢

- [Mihomo](https://github.com/MetaCubeX/mihomo) - 本项目服务的核心组件
- [Yacd](https://github.com/haishanh/yacd) - 优秀的Clash Web控制面板 