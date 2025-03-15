# Mihomo自动更新服务 - Docker版

本文档提供使用Docker部署Mihomo自动更新服务的说明。

## 目录结构

```
.
├── backend/            # 后端代码
├── frontend/           # 前端代码
├── config/             # 配置文件目录(将被挂载)
├── logs/               # 日志文件目录(将被挂载)
├── docker-compose.yml  # Docker Compose配置文件
└── README.docker.md    # Docker说明文档
```

## 快速开始

### 前提条件

- Docker 19.03+
- Docker Compose 1.25+
- Mihomo（Clash.Meta）已安装在宿主机的`/etc/mihomo`目录

### 首次部署

1. 克隆仓库并进入项目目录:

```bash
git clone https://github.com/yourusername/mihomo-updater.git
cd mihomo-updater
```

2. 创建必要的目录:

```bash
mkdir -p config logs
```

3. 使用Docker Compose构建并启动服务:

```bash
docker-compose up -d
```

首次启动时，系统会:
- 自动构建前端和后端镜像
- 如果`config`目录中没有配置文件，将使用默认配置
- 将前端服务暴露在3000端口，后端服务暴露在5000端口

4. 访问Web界面:

```
http://your-server-ip:3000
```

### 配置文件

容器启动时会检查`./config/config.yaml`是否存在:
- 如果存在，使用已有配置文件
- 如果不存在，将复制默认配置文件

配置文件会被持久化到宿主机的`./config`目录，可以直接编辑:

```bash
nano config/config.yaml
```

修改配置后，重启容器使配置生效:

```bash
docker-compose restart
```

### 日志文件

日志文件存储在宿主机的`./logs`目录中:

```bash
tail -f logs/app.log
```

## 高级配置

### 修改端口

如需修改暴露的端口，编辑`docker-compose.yml`文件:

```yaml
services:
  backend:
    ports:
      - "自定义端口:5000"  # 修改为你想要的端口
  
  frontend:
    ports:
      - "自定义端口:80"    # 修改为你想要的端口
```

### 自定义Mihomo目录

如果Mihomo不在默认的`/etc/mihomo`目录，修改`docker-compose.yml`中的卷挂载:

```yaml
services:
  backend:
    volumes:
      - ./config:/config
      - ./logs:/app/logs
      - /你的自定义目录:/etc/mihomo
```

## 故障排除

### 容器无法启动

检查日志:

```bash
docker-compose logs
```

### 无法连接到后端API

确保后端容器正在运行:

```bash
docker-compose ps
```

### 配置未生效

确保修改了正确的配置文件，并重启了容器:

```bash
docker-compose restart
```

## 更新容器

拉取最新代码并重新构建:

```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
``` 