# Mihomo自动更新服务

一个用于自动更新Mihomo（Clash.Meta）配置文件和GeoIP数据的服务，具有美观的Web界面管理。

## 功能特点

- 自动定期从指定URL拉取最新的Clash配置文件
- 智能合并配置文件，只更新`proxies`、`proxy-groups`、`rules`部分
- 自动备份原配置文件，并管理备份数量
- 定期更新GeoIP、GeoSite和MMDB数据文件
- 提供美观的响应式Web界面，支持PC和移动设备
- 提供手动更新按钮，便于立即更新
- 记录更新历史和详细日志
- 允许通过Web界面修改配置项
- 支持一键跳转到Yacd面板
- 自动日志管理，每个日志文件最大10MB，最多保留10个文件

## 安装方法

### 系统要求

- Linux系统（已在Ubuntu、Debian上测试）
- Python 3.6+
- Mihomo（Clash.Meta）已配置为系统服务

### 步骤一：下载代码

```bash
git clone https://github.com/zztdandan/mihomo-updater.git
cd mihomo-updater
```

### 步骤二：安装环境

运行安装脚本来配置所需的环境：

```bash
sudo chmod +x install.sh
sudo ./install.sh
```

安装脚本会自动：
- 配置APT国内源（清华大学镜像）
- 配置pip国内源（清华大学镜像） 
- 配置npm国内源（淘宝镜像）
- 安装Python、Node.js和其他依赖
- 安装项目的Python依赖

### 步骤三：前端构建

```bash
cd frontend
npm install
npm run build
cd ..
```

### 步骤四：启动服务

在开发环境中可以直接运行：

```bash
# 启动后端
cd backend
python3 app.py

# 在另一个终端启动前端开发服务器
cd frontend
npm run dev
```

### 部署为系统服务（可选）

如果想将应用部署为系统服务，请按照以下步骤操作：

1. 创建系统服务配置文件：

```bash
sudo nano /etc/systemd/system/mihomo-updater.service
```

2. 添加以下内容（请根据实际路径进行调整）：

```
[Unit]
Description=Mihomo Updater Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/mihomo-updater/backend
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. 启用并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable mihomo-updater.service
sudo systemctl start mihomo-updater.service
```

## 配置文件说明

配置文件位于 `backend/config.yaml`，包含以下关键选项：

- `fetch_url`：拉取Clash配置的URL
- `fetch_interval`：Clash配置更新间隔（秒）
- `geoip_fetch_interval`：GeoIP数据更新间隔（秒）
- `mihomo_config_path`：Mihomo配置文件路径
- `backup_dir`：备份目录
- `geoip_url`/`geosite_url`/`mmdb_url`：GeoIP相关数据下载地址
- `yacd_url`/`clash_api_url`：Yacd和Clash API地址
- `web_port`：Web界面监听端口

## 使用方法

### Web界面

启动服务后，可通过以下地址访问Web界面：

- 开发模式: `http://your-server-ip:3000`
- 生产模式: `http://your-server-ip:5000`

### Web界面功能

- **配置管理**：查看和修改服务配置
- **手动更新**：手动触发配置或GeoIP更新
- **更新历史**：查看历史更新记录及状态
- **跳转Yacd**：一键跳转到Mihomo管理界面

### 命令行控制

如果配置为系统服务，可使用标准的systemd命令控制：

```bash
# 启动服务
sudo systemctl start mihomo-updater.service

# 停止服务
sudo systemctl stop mihomo-updater.service

# 重启服务
sudo systemctl restart mihomo-updater.service

# 查看服务状态
sudo systemctl status mihomo-updater.service
```

## 开发指南

### 后端开发

后端使用Python和Flask开发，位于`backend`目录。

```bash
cd backend
python3 app.py
```

### 前端开发

前端使用Vue 3、TypeScript和Naive UI开发，位于`frontend`目录。

```bash
cd frontend
npm install
npm run dev
```

前端支持热重载，任何修改都会立即反映在浏览器中。更多信息请参考`frontend/README.md`。

## 日志文件

日志文件位于 `backend/logs/` 目录下：

- `app.log`：主应用日志
- `updater.log`：配置更新器日志
- `geoip_updater.log`：GeoIP更新器日志

日志文件采用自动轮转机制：
- 每个日志文件最大大小为10MB
- 每个日志类型最多保留10个历史文件（例如：app.log.1, app.log.2, ...）
- 不再输出到系统日志中，方便直接查看日志内容

查看日志命令示例：

```bash
# 查看主应用日志
cat backend/logs/app.log

# 实时监控日志变化
tail -f backend/logs/app.log
```

## 故障排除

如果遇到问题，请检查：

1. 后端运行状态：检查日志文件内容
2. 前端构建问题：检查前端构建是否成功
3. 配置文件：确保配置文件格式正确，所有路径都正确设置
4. 网络连接：确保能够访问配置URL和GeoIP下载URL

### 常见问题

#### 前端无法连接到后端API

确保后端已经启动，且在开发模式下前端Vite配置了正确的代理。

#### 远程开发中找不到文件

如果在远程开发中报错找不到`main.js`等文件，可能是TypeScript相关的问题。尝试运行：

```bash
cd frontend
npm run dev:force
```

或参考`frontend/README.md`中的故障排除部分。

## 许可证

MIT 

## 项目结构

```
project-root/
├── frontend/             # 前端TypeScript代码
│   ├── src/              # 前端源代码
│   ├── public/           # 静态资源
│   └── ...
├── backend/              # 后端Python代码
│   ├── app.py            # 主应用文件
│   ├── requirements.txt  # Python依赖
│   └── ...
├── build/                # 打包相关文件
│   ├── docker/           # Docker相关配置
│   │   ├── frontend/     # 前端Docker配置
│   │   └── backend/      # 后端Docker配置
│   ├── scripts/          # 构建脚本
│   ├── docker-compose.yml # Docker编排配置
│   └── ...
├── config/               # 应用配置文件
└── docs/                 # 项目文档
    ├── README.md         # 详细文档
    ├── docker-guide.md   # Docker部署指南
    └── frontend.md       # 前端文档
```

## 快速开始

详细使用方法请参考 `docs/` 目录下的相关文档。

### 使用脚本安装

```bash
# 安装项目
bash build/scripts/install.sh

# 准备环境
bash build/scripts/prepare.sh
```

### 使用Docker部署

```bash
# 安装Docker和Docker Compose
bash build/scripts/install-docker-compose.sh

# 启动服务
docker-compose -f build/docker-compose.yml up -d
```

## 文档

- [详细使用文档](docs/README.md)
- [Docker部署指南](docs/docker-guide.md)
- [前端开发文档](docs/frontend.md) 