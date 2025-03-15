#!/bin/bash

# 显示欢迎信息
echo "==============================================="
echo "    Mihomo自动更新服务 - Docker环境准备脚本"
echo "==============================================="

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# 检查是否以root权限运行
if [ "$(id -u)" != "0" ]; then
   echo "此脚本需要root权限" 
   echo "请使用 sudo bash build/scripts/prepare-docker.sh 运行"
   exit 1
fi

# 创建Docker数据目录
create_docker_directories() {
    echo "创建Docker数据目录..."
    # mkdir -p /etc/mihomo/mihomo-updater/data
    # chmod -R 755 /etc/mihomo/mihomo-updater/data
    
    # 创建本地数据目录
    mkdir -p "${PROJECT_ROOT}/data"
    
    echo "✅ Docker数据目录创建完成"
}

# 检查并安装Docker
install_docker() {
    echo "检查Docker安装状态..."
    
    # 检查Docker是否已安装
    if command -v docker &> /dev/null; then
        echo "✅ Docker已安装"
    else
        echo "安装Docker..."
        
        # 安装依赖
        apt update
        apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
        
        # 添加Docker官方GPG密钥
        mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        
        # 设置Docker APT仓库
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
        
        # 更新APT索引并安装Docker
        apt update
        apt install -y docker-ce docker-ce-cli containerd.io
        
        # 启动Docker服务
        systemctl enable docker
        systemctl start docker
        
        echo "✅ Docker安装完成"
    fi
}

# 检查并安装Docker Compose
install_docker_compose() {
    echo "检查Docker Compose安装状态..."
    
    # 检查Docker Compose是否已安装
    if command -v docker-compose &> /dev/null; then
        echo "✅ Docker Compose已安装"
    else
        echo "安装Docker Compose..."
        
        # 获取最新版本的Docker Compose
        COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
        
        # 如果无法获取版本，使用默认版本
        if [ -z "$COMPOSE_VERSION" ]; then
            COMPOSE_VERSION="v2.23.0"
        fi
        
        # 下载Docker Compose二进制文件
        curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        
        # 设置可执行权限
        chmod +x /usr/local/bin/docker-compose
        
        # 创建软链接
        ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
        
        echo "✅ Docker Compose安装完成"
    fi
}

# 构建Docker镜像
build_docker_images() {
    echo "构建Docker镜像..."
    
    # 确保Docker服务正在运行
    systemctl start docker
    
    # 检查Dockerfile是否存在
    if [ ! -f "build/docker/backend/Dockerfile" ] || [ ! -f "build/docker/frontend/Dockerfile" ]; then
        echo "❌ Dockerfile不存在，请先确保已运行编译准备脚本"
        exit 1
    fi
    
    # 构建Docker镜像
    docker-compose -f build/docker-compose.yml build
    
    echo "✅ Docker镜像构建完成"
}

# 启动Docker容器
start_docker_containers() {
    echo "启动Docker容器..."
    
    docker-compose -f build/docker-compose.yml up -d
    
    echo "✅ Docker容器已启动"
}

# 添加到系统服务
setup_system_service() {
    echo "设置系统服务..."
    
    # 创建服务文件
    cat > /etc/systemd/system/mihomo-updater.service << EOF
[Unit]
Description=Mihomo Updater Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=${PROJECT_ROOT}
ExecStart=/usr/bin/docker-compose -f ${PROJECT_ROOT}/build/docker-compose.yml up -d
ExecStop=/usr/bin/docker-compose -f ${PROJECT_ROOT}/build/docker-compose.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF
    
    # 重新加载systemd
    systemctl daemon-reload
    
    # 启用服务
    systemctl enable mihomo-updater.service
    
    echo "✅ 系统服务设置完成"
}

# 打印使用说明
print_usage_guide() {
    echo "==============================================="
    echo "      Mihomo自动更新服务 - 使用指南"
    echo "==============================================="
    echo "服务已成功部署！"
    echo ""
    echo "访问地址:"
    echo "- 前端界面: http://$(hostname -I | awk '{print $1}'):3000"
    echo "- 后端API: http://$(hostname -I | awk '{print $1}'):5000"
    echo "- Yacd面板: http://$(hostname -I | awk '{print $1}'):8080"
    echo ""
    echo "服务管理命令:"
    echo "- 启动服务: sudo systemctl start mihomo-updater"
    echo "- 停止服务: sudo systemctl stop mihomo-updater"
    echo "- 重启服务: sudo systemctl restart mihomo-updater"
    echo "- 查看状态: sudo systemctl status mihomo-updater"
    echo ""
    echo "手动操作Docker命令:"
    echo "- 启动容器: docker-compose -f ${PROJECT_ROOT}/build/docker-compose.yml up -d"
    echo "- 停止容器: docker-compose -f ${PROJECT_ROOT}/build/docker-compose.yml down"
    echo "- 查看日志: docker-compose -f ${PROJECT_ROOT}/build/docker-compose.yml logs"
    echo "==============================================="
}

# 主函数
main() {
    create_docker_directories
    install_docker
    install_docker_compose
    build_docker_images
    start_docker_containers
    setup_system_service
    print_usage_guide
}

# 执行主函数
main 