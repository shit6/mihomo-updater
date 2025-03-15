# Mihomo自动更新服务 - Docker部署指南

本文档提供使用Docker部署Mihomo自动更新服务的详细说明。

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

## 部署方法

以下提供两种Docker部署方式，根据您的需求选择合适的方法。

### 方式一：在项目目录中构建并运行

这种方式适合需要查看或修改源代码的用户。

1. 克隆仓库并进入项目目录：

```bash
git clone https://github.com/zztdandan/mihomo-updater.git
cd mihomo-updater
```

2. 使用Docker Compose构建镜像：

```bash
docker-compose -f build/docker-compose.build.yml build
```

3. 启动服务：

```bash
docker-compose -f build/docker-compose.yml up -d
```

### 方式二：在任意目录运行预构建镜像

这种方式适合只需要运行服务，不需要修改源码的用户。

1. 首先在原项目目录构建镜像：

```bash
# 如果您没有源码，首先克隆仓库
git clone https://github.com/zztdandan/mihomo-updater.git
cd mihomo-updater

# 在项目目录中构建镜像
docker-compose -f build/docker-compose.build.yml build
```

2. 复制`build/docker-compose.yml`文件到任意目录：

```bash
mkdir -p ~/mihomo-service
cp build/docker-compose.yml ~/mihomo-service/
cd ~/mihomo-service
```

3. 在新目录中启动服务：

```bash
docker-compose up -d
```

## 环境变量配置

服务支持通过环境变量自定义各种文件路径，可以在启动命令前设置，或在`docker-compose.yml`中配置：

```bash
# 自定义数据目录和配置文件路径
MIHOMO_DATA_DIR=/path/to/data \
MIHOMO_CONFIG_FILE=/path/to/config.yaml \
MIHOMO_GEOIP_FILE=/path/to/geoip.dat \
MIHOMO_GEOSITE_FILE=/path/to/geosite.dat \
MIHOMO_COUNTRY_FILE=/path/to/country.mmdb \
docker-compose up -d
```

### 默认路径

如果不指定环境变量，系统将使用以下默认值：

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| MIHOMO_DATA_DIR | ./data | 数据目录 |
| MIHOMO_CONFIG_FILE | /etc/mihomo/config.yaml | 配置文件路径 |
| MIHOMO_GEOIP_FILE | /etc/mihomo/geoip.dat | GeoIP文件路径 |
| MIHOMO_GEOSITE_FILE | /etc/mihomo/geosite.dat | GeoSite文件路径 |
| MIHOMO_COUNTRY_FILE | /etc/mihomo/country.mmdb | MMDB文件路径 |

## 容器说明

服务由三个容器组成：

| 容器名 | 作用 | 默认端口 |
|--------|------|----------|
| mihomo-backend | 后端服务，负责配置更新和数据管理 | 5000 |
| mihomo-frontend | 前端界面，提供Web操作界面 | 3000 |
| mihomo-yacd | Yacd面板，Mihomo的Web控制面板 | 8080 |

## 端口配置

如需修改暴露的端口，编辑`docker-compose.yml`文件：

```yaml
services:
  backend:
    ports:
      - "自定义端口:5000"  # 修改为您想要的端口
  
  frontend:
    ports:
      - "自定义端口:80"    # 修改为您想要的端口
      
  yacd:
    ports:
      - "自定义端口:80"    # 修改为您想要的端口
```

## 持久化存储

容器使用的数据都会被持久化到主机目录：

1. 如果使用默认配置，数据将存储在`./data`目录（相对于docker-compose.yml文件位置）
2. 如果设置了`MIHOMO_DATA_DIR`环境变量，数据将存储在指定目录

## 日志查看

查看容器日志：

```bash
# 查看所有容器日志
docker-compose logs

# 查看特定容器日志
docker-compose logs backend

# 实时跟踪日志
docker-compose logs -f backend
```

## 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps
```

## 更新服务

### 更新方式一：在原项目目录

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose -f build/docker-compose.build.yml build --no-cache

# 重启服务
docker-compose -f build/docker-compose.yml down
docker-compose -f build/docker-compose.yml up -d
```

### 更新方式二：在其他目录

1. 在原项目目录重新构建镜像：

```bash
# 进入原项目目录
cd /path/to/mihomo-updater

# 拉取最新代码
git pull

# 重新构建镜像
docker-compose -f build/docker-compose.build.yml build --no-cache
```

2. 在部署目录重启服务：

```bash
# 进入部署目录
cd ~/mihomo-service

# 重启服务
docker-compose down
docker-compose up -d
```

## 故障排除

### 容器无法启动

**问题**：容器启动失败。

**解决方法**：
1. 检查日志：`docker-compose logs`
2. 检查端口占用：`netstat -tulpn | grep <端口号>`
3. 检查目录权限：确保挂载目录有正确的读写权限

### 无法连接到服务

**问题**：无法通过浏览器访问服务。

**解决方法**：
1. 确保容器正在运行：`docker-compose ps`
2. 检查防火墙设置：确保端口已开放
3. 使用`curl localhost:<端口>`测试本地连接

### 配置更新失败

**问题**：配置更新失败。

**解决方法**：
1. 检查容器日志：`docker-compose logs backend`
2. 确保宿主机的配置文件路径正确且有权限访问
3. 检查网络连接：确保容器可以访问外网

## 高级配置

### 使用自定义网络

如果需要将服务与其他Docker容器集成，可以使用自定义网络：

```yaml
networks:
  mihomo-net:
    driver: bridge

services:
  backend:
    # ...其他配置...
    networks:
      - mihomo-net
  
  frontend:
    # ...其他配置...
    networks:
      - mihomo-net
      
  yacd:
    # ...其他配置...
    networks:
      - mihomo-net
```

### 设置自动启动

确保Docker服务配置为开机自启，服务会随Docker自动启动：

```bash
# 设置Docker开机自启
sudo systemctl enable docker

# 确认Docker状态
sudo systemctl status docker
``` 