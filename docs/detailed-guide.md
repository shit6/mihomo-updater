# Mihomo自动更新服务 - 详细指南

本文档提供Mihomo自动更新服务的完整安装和使用指南。

## 系统要求

- Linux系统（已在Ubuntu、Debian上测试）
- Python 3.6+
- Mihomo（Clash.Meta）已配置为系统服务

## 安装方法

### 方法一：Docker部署（推荐）

请参考[Docker部署指南](docker-guide.md)获取详细的Docker部署说明。

### 方法二：系统直接安装

#### 步骤一：下载代码

```bash
git clone https://github.com/zztdandan/mihomo-updater.git
cd mihomo-updater
```

#### 步骤二：安装环境

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

#### 步骤三：前端构建

```bash
cd frontend
npm install
npm run build
cd ..
```

#### 步骤四：启动服务

在开发环境中可以直接运行：

```bash
# 启动后端
cd backend
python3 app.py

# 在另一个终端启动前端开发服务器
cd frontend
npm run dev
```

### 部署为系统服务

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

## 配置文件详解

配置文件位于 `backend/config.yaml`，包含以下选项：

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `fetch_url` | 拉取Clash配置的URL | - |
| `fetch_interval` | Clash配置更新间隔（秒） | 3600 |
| `geoip_fetch_interval` | GeoIP数据更新间隔（秒） | 86400 |
| `mihomo_config_path` | Mihomo配置文件路径 | /etc/mihomo/config.yaml |
| `backup_dir` | 备份目录 | /etc/mihomo/backups |
| `max_backups` | 最大备份数量 | 10 |
| `geoip_url` | GeoIP数据下载地址 | https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geoip.dat |
| `geosite_url` | GeoSite数据下载地址 | https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geosite.dat |
| `mmdb_url` | MMDB数据下载地址 | https://github.com/Loyalsoldier/geoip/releases/latest/download/Country.mmdb |
| `yacd_url` | Yacd访问地址 | http://localhost:8080 |
| `clash_api_url` | Clash API地址 | http://localhost:9090 |
| `web_port` | Web界面监听端口 | 5000 |

## 详细使用说明

### Web界面功能

启动服务后，可通过`http://your-server-ip:5000`访问Web界面，主要功能包括：

#### 配置管理

- **查看配置**：显示当前所有配置项
- **修改配置**：可直接在Web界面修改配置项，保存后自动生效
- **重置配置**：将配置恢复到默认值

#### 手动更新

- **更新配置**：立即从配置URL拉取并更新配置
- **更新GeoIP**：立即更新GeoIP、GeoSite和MMDB数据文件

#### 更新历史

- 显示所有配置更新记录，包括时间、状态和详情
- 支持查看每次更新的详细日志

#### 跳转Yacd

- 一键跳转到Yacd管理面板，方便进行Mihomo的直接管理

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

## 日志管理

日志文件位于 `backend/logs/` 目录下：

- `app.log`：主应用日志
- `updater.log`：配置更新器日志
- `geoip_updater.log`：GeoIP更新器日志

日志文件采用自动轮转机制：
- 每个日志文件最大大小为10MB
- 每个日志类型最多保留10个历史文件（例如：app.log.1, app.log.2, ...）

查看日志命令示例：

```bash
# 查看主应用日志
cat backend/logs/app.log

# 实时监控日志变化
tail -f backend/logs/app.log
```

## 故障排除

### 常见问题

#### 前端无法连接到后端API

**问题**：Web界面显示"无法连接到后端API"错误。

**解决方法**：
1. 确保后端已经启动：`systemctl status mihomo-updater.service`
2. 检查防火墙设置：`sudo ufw status` 并确保开放了5000端口
3. 检查后端日志：`cat backend/logs/app.log`

#### 配置更新失败

**问题**：配置更新显示失败，但没有明显错误。

**解决方法**：
1. 检查配置URL是否可访问：`curl -I [your_fetch_url]`
2. 检查更新器日志：`cat backend/logs/updater.log`
3. 检查权限问题：确保应用有权限读写配置文件

#### GeoIP更新失败

**问题**：GeoIP数据更新失败。

**解决方法**：
1. 检查网络连接：`ping github.com`
2. 检查GeoIP更新器日志：`cat backend/logs/geoip_updater.log`
3. 尝试手动下载并检查URL是否有效

#### 远程开发中找不到文件

**问题**：在远程开发中报错找不到`main.js`等文件。

**解决方法**：
这可能是TypeScript相关的问题。尝试运行：

```bash
cd frontend
npm run dev:force
```

或参考`frontend/README.md`中的故障排除部分。

## 高级使用

### 自定义备份策略

如果需要更改备份策略，可以修改配置文件中的`max_backups`选项。例如：

```yaml
max_backups: 20  # 保留20个备份文件
```

### 多实例部署

如果需要为多个Mihomo实例提供更新服务，可以：

1. 复制项目到不同目录
2. 修改各自的配置文件，特别是端口和文件路径
3. 分别启动各个实例

## 更新与维护

### 更新项目代码

```bash
cd /path/to/mihomo-updater
git pull
```

如果使用Docker部署，需要重新构建镜像：

```bash
docker-compose -f build/docker-compose.build.yml build --no-cache
docker-compose -f build/docker-compose.yml down
docker-compose -f build/docker-compose.yml up -d
```

### 清理日志和备份

```bash
# 清理过多的日志文件
find backend/logs -name "*.log.*" -type f -delete

# 手动清理备份文件
find /etc/mihomo/backups -name "config_*.yaml" -type f | sort | head -n -10 | xargs rm -f
``` 