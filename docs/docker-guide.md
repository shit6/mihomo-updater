# Mihomo自动更新服务 - Docker版

本文档提供使用Docker部署Mihomo自动更新服务的说明。

## 目录结构

```
.
├── backend/                  # 后端代码
├── frontend/                 # 前端代码
├── build/                    # 构建相关配置
│   ├── docker-compose.yml    # 运行服务的Docker Compose配置
│   └── docker-compose.build.yml # 构建镜像的Docker Compose配置
└── data/                     # 数据目录(将被挂载)
```

## 快速开始

### 前提条件

- Docker 19.03+
- Docker Compose 1.25+
- Mihomo（Clash.Meta）已安装在宿主机的默认目录（可自定义）

### 使用方法（两种方式）

#### 方式一：在项目目录中构建并运行

1. 克隆仓库并进入项目目录:

```bash
git clone https://github.com/zztdandan/mihomo-updater.git
cd mihomo-updater
```

2. 使用Docker Compose构建镜像:

```bash
docker-compose -f build/docker-compose.build.yml build
```

3. 启动服务:

```bash
docker-compose -f build/docker-compose.yml up -d
```

#### 方式二：在任意目录运行预构建镜像

1. 首先在原项目目录构建镜像:

```bash
# 在项目目录中
docker-compose -f build/docker-compose.build.yml build
```

2. 复制`build/docker-compose.yml`文件到任意目录:

```bash
mkdir -p ~/mihomo-service
cp build/docker-compose.yml ~/mihomo-service/
cd ~/mihomo-service
```

3. 在新目录中启动服务:

```bash
docker-compose up -d
```

### 配置自定义路径

服务支持通过环境变量自定义各种文件路径：

```bash
# 自定义数据目录和配置文件路径
MIHOMO_DATA_DIR=/path/to/data \
MIHOMO_CONFIG_FILE=/path/to/config.yaml \
MIHOMO_GEOIP_FILE=/path/to/geoip.dat \
MIHOMO_GEOSITE_FILE=/path/to/geosite.dat \
MIHOMO_COUNTRY_FILE=/path/to/country.mmdb \
docker-compose up -d
```

如果不指定这些环境变量，则使用默认值：
- 数据目录：`./data`（相对于docker-compose.yml文件位置）
- 配置文件：`/etc/mihomo/config.yaml`（宿主机路径）
- GeoIP文件：`/etc/mihomo/geoip.dat`（宿主机路径）
- GeoSite文件：`/etc/mihomo/geosite.dat`（宿主机路径）
- Country文件：`/etc/mihomo/country.mmdb`（宿主机路径）

### 访问Web界面

服务启动后，可以通过以下地址访问Web界面：

- 前端界面: `http://your-server-ip:3000`
- Yacd界面: `http://your-server-ip:8080`

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
      
  yacd:
    ports:
      - "自定义端口:80"    # 修改为你想要的端口
```

## 持久化数据

容器使用的数据都会被持久化：

1. 如果使用默认配置，数据将存储在`./data`目录（相对于docker-compose.yml文件位置）
2. 如果设置了`MIHOMO_DATA_DIR`环境变量，数据将存储在指定目录

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

## 更新服务

### 更新方式一：在原项目目录

```bash
git pull
docker-compose -f build/docker-compose.build.yml build --no-cache
docker-compose -f build/docker-compose.yml down
docker-compose -f build/docker-compose.yml up -d
```

### 更新方式二：在其他目录

1. 在原项目目录重新构建镜像:

```bash
git pull
docker-compose -f build/docker-compose.build.yml build --no-cache
```

2. 在部署目录重启服务:

```bash
docker-compose down
docker-compose up -d
```

这将使用新构建的镜像启动服务，同时保留所有数据和配置。 