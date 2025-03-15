#!/bin/bash

# 显示欢迎信息
echo "==============================================="
echo "     Mihomo自动更新服务 - 编译环境准备脚本"
echo "==============================================="

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# 检查是否以root权限运行
if [ "$(id -u)" != "0" ]; then
   echo "此脚本需要root权限" 
   echo "请使用 sudo bash build/scripts/prepare-build.sh 运行"
   exit 1
fi

# 用户交互函数
ask_user() {
    local step_name=$1
    local check_result=$2
    
    echo ""
    echo "步骤: $step_name"
    echo "检查结果: $check_result"
    echo ""
    echo "请选择操作:"
    echo "1) 自动执行此步骤"
    echo "2) 跳过此步骤"
    echo "3) 显示手动执行的命令"
    read -p "请输入选项 [1-3]: " choice
    
    case $choice in
        1) return 0 ;; # 自动执行
        2) return 1 ;; # 跳过
        3) return 2 ;; # 显示命令
        *) echo "无效选项，默认自动执行"; return 0 ;;
    esac
}

# 创建必要的目录结构
create_directories() {
    echo "检查目录结构..."
    
    local missing_dirs=()
    
    # 检查各个目录是否存在
    [ ! -d "config" ] && missing_dirs+=("config")
    [ ! -d "data/logs" ] && missing_dirs+=("data/logs")
    [ ! -d "frontend/dist" ] && missing_dirs+=("frontend/dist")
    [ ! -d "backend/logs" ] && missing_dirs+=("backend/logs")
    
    # 准备检查结果消息
    if [ ${#missing_dirs[@]} -eq 0 ]; then
        local check_result="✅ 所有必要的目录已存在"
    else
        local check_result="⚠️ 以下目录不存在: ${missing_dirs[*]}"
    fi
    
    # 询问用户
    ask_user "创建必要的目录结构" "$check_result"
    local user_choice=$?
    
    case $user_choice in
        0) # 自动执行
            echo "创建必要的目录结构..."
            mkdir -p config data/logs frontend/dist backend/logs
            echo "✅ 目录结构创建完成"
            ;;
        1) # 跳过
            echo "跳过目录创建步骤"
            ;;
        2) # 显示命令
            echo "要手动创建目录，请执行以下命令:"
            echo "mkdir -p config data/logs frontend/dist backend/logs"
            read -p "按回车键继续..." dummy
            ;;
    esac
}

# 配置APT国内源
setup_apt_mirrors() {
    echo "检查APT国内源配置..."
    
    # 检测是否已经配置过清华源
    if grep -q "mirrors.tuna.tsinghua.edu.cn" /etc/apt/sources.list; then
        local check_result="✅ APT国内源已配置为清华大学镜像"
    else
        local check_result="⚠️ APT国内源未配置为清华大学镜像"
    fi
    
    # 询问用户
    ask_user "配置APT国内源(清华大学镜像)" "$check_result"
    local user_choice=$?
    
    case $user_choice in
        0) # 自动执行
            if grep -q "mirrors.tuna.tsinghua.edu.cn" /etc/apt/sources.list; then
                echo "✅ APT国内源已配置，无需操作"
                return 0
            fi
            
            echo "配置APT国内源(清华大学镜像)..."
            # 备份原始sources.list
            cp /etc/apt/sources.list /etc/apt/sources.list.bak.$(date +%Y%m%d%H%M%S)
            
            # 检测系统版本
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                DISTRO=$ID
                VERSION=$VERSION_ID
                
                case $DISTRO in
                    ubuntu)
                        echo "检测到Ubuntu系统，版本: $VERSION"
                        cat > /etc/apt/sources.list << EOF
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $(lsb_release -cs) main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $(lsb_release -cs)-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $(lsb_release -cs)-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $(lsb_release -cs)-security main restricted universe multiverse
EOF
                        ;;
                    debian)
                        echo "检测到Debian系统，版本: $VERSION"
                        cat > /etc/apt/sources.list << EOF
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ $(lsb_release -cs) main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ $(lsb_release -cs)-updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ $(lsb_release -cs)-backports main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security $(lsb_release -cs)-security main contrib non-free
EOF
                        ;;
                    *)
                        echo "⚠️ 不支持的Linux发行版: $DISTRO"
                        echo "跳过APT源配置，请手动配置适合您系统的APT源"
                        return 0
                        ;;
                esac
                
                # 更新APT缓存
                apt update
                echo "✅ APT国内源配置完成"
            else
                echo "⚠️ 无法检测系统版本，跳过APT源配置"
            fi
            ;;
        1) # 跳过
            echo "跳过APT国内源配置步骤"
            ;;
        2) # 显示命令
            echo "要手动配置APT国内源，请执行以下操作:"
            echo "1. 备份当前源: cp /etc/apt/sources.list /etc/apt/sources.list.bak"
            echo "2. 编辑源文件: nano /etc/apt/sources.list"
            echo "3. 对于Ubuntu系统，添加以下内容:"
            echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ \$(lsb_release -cs) main restricted universe multiverse"
            echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ \$(lsb_release -cs)-updates main restricted universe multiverse"
            echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ \$(lsb_release -cs)-backports main restricted universe multiverse"
            echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ \$(lsb_release -cs)-security main restricted universe multiverse"
            echo "4. 对于Debian系统，添加以下内容:"
            echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ \$(lsb_release -cs) main contrib non-free"
            echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ \$(lsb_release -cs)-updates main contrib non-free"
            echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ \$(lsb_release -cs)-backports main contrib non-free"
            echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security \$(lsb_release -cs)-security main contrib non-free"
            echo "5. 更新APT缓存: apt update"
            read -p "按回车键继续..." dummy
            ;;
    esac
}

# 配置pip国内源
setup_pip_mirrors() {
    echo "检查pip国内源配置..."
    
    # 检测是否已配置pip源
    if [ -f ~/.pip/pip.conf ] && grep -q "mirrors.tuna.tsinghua.edu.cn" ~/.pip/pip.conf; then
        local check_result="✅ pip国内源已配置为清华大学镜像"
    else
        local check_result="⚠️ pip国内源未配置为清华大学镜像"
    fi
    
    # 询问用户
    ask_user "配置pip国内源(清华大学镜像)" "$check_result"
    local user_choice=$?
    
    case $user_choice in
        0) # 自动执行
            if [ -f ~/.pip/pip.conf ] && grep -q "mirrors.tuna.tsinghua.edu.cn" ~/.pip/pip.conf; then
                echo "✅ pip国内源已配置，无需操作"
                return 0
            fi
            
            echo "配置pip国内源(清华大学镜像)..."
            # 创建pip配置目录
            mkdir -p ~/.pip
            
            # 配置pip源
            cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
            echo "✅ pip国内源配置完成"
            ;;
        1) # 跳过
            echo "跳过pip国内源配置步骤"
            ;;
        2) # 显示命令
            echo "要手动配置pip国内源，请执行以下操作:"
            echo "1. 创建pip配置目录: mkdir -p ~/.pip"
            echo "2. 创建配置文件: nano ~/.pip/pip.conf"
            echo "3. 添加以下内容:"
            echo "[global]"
            echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple"
            echo "[install]"
            echo "trusted-host = pypi.tuna.tsinghua.edu.cn"
            read -p "按回车键继续..." dummy
            ;;
    esac
}

# 配置npm国内源
setup_npm_mirrors() {
    echo "检查npm国内源配置..."
    
    # 检测npm是否安装
    if ! command -v npm &> /dev/null; then
        local check_result="⚠️ npm未安装，无法配置npm国内源"
        
        # 询问用户
        ask_user "配置npm国内源(淘宝镜像)" "$check_result"
        local user_choice=$?
        
        case $user_choice in
            0|1) # 自动执行或跳过
                echo "跳过npm国内源配置步骤（npm未安装）"
                return 0
                ;;
            2) # 显示命令
                echo "要安装npm并配置国内源，请执行以下操作:"
                echo "1. 安装Node.js和npm: apt install -y nodejs npm"
                echo "2. 配置npm淘宝源: npm config set registry https://registry.npmmirror.com"
                read -p "按回车键继续..." dummy
                return 0
                ;;
        esac
    fi
    
    # 检测是否已配置npm源
    if npm config get registry | grep -q "registry.npmmirror.com"; then
        local check_result="✅ npm国内源已配置为淘宝镜像"
    else
        local check_result="⚠️ npm国内源未配置为淘宝镜像"
    fi
    
    # 询问用户
    ask_user "配置npm国内源(淘宝镜像)" "$check_result"
    local user_choice=$?
    
    case $user_choice in
        0) # 自动执行
            if npm config get registry | grep -q "registry.npmmirror.com"; then
                echo "✅ npm国内源已配置，无需操作"
                return 0
            fi
            
            echo "配置npm国内源(淘宝镜像)..."
            # 配置npm淘宝源
            npm config set registry https://registry.npmmirror.com
            echo "✅ npm国内源配置完成"
            ;;
        1) # 跳过
            echo "跳过npm国内源配置步骤"
            ;;
        2) # 显示命令
            echo "要手动配置npm国内源，请执行以下命令:"
            echo "npm config set registry https://registry.npmmirror.com"
            read -p "按回车键继续..." dummy
            ;;
    esac
}

# 检查并安装必要的软件包
install_dependencies() {
    echo "检查必要的软件包..."
    
    local missing_deps=()
    
    # 检查基本工具
    ! command -v curl &> /dev/null && missing_deps+=("curl")
    ! command -v wget &> /dev/null && missing_deps+=("wget")
    ! command -v git &> /dev/null && missing_deps+=("git")
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        missing_deps+=("nodejs")
    elif [ "$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)" -lt 14 ]; then
        missing_deps+=("nodejs-upgrade")
    fi
    
    # 准备检查结果消息
    if [ ${#missing_deps[@]} -eq 0 ]; then
        local check_result="✅ 所有必要的软件包已安装"
    else
        local check_result="⚠️ 以下软件包需要安装或升级: ${missing_deps[*]}"
    fi
    
    # 询问用户
    ask_user "安装必要的软件包" "$check_result"
    local user_choice=$?
    
    case $user_choice in
        0) # 自动执行
            if [ ${#missing_deps[@]} -eq 0 ]; then
                echo "✅ 所有必要的软件包已安装，无需操作"
                return 0
            fi
            
            echo "安装必要的软件包..."
            
            # 安装基本工具
            apt update
            apt install -y curl wget git
            
            # 检查Python
            if ! command -v python3 &> /dev/null; then
                echo "安装Python3..."
                apt install -y python3 python3-pip python3-venv
            else
                echo "✅ Python3已安装"
            fi
            
            # 检查Node.js
            if ! command -v node &> /dev/null; then
                echo "安装Node.js和npm..."
                apt install -y nodejs npm
            else
                echo "✅ Node.js已安装"
            fi
            
            # 检查Node.js版本，如果低于14，安装最新的LTS版本
            if command -v node &> /dev/null; then
                NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
                if [ "$NODE_VERSION" -lt 14 ]; then
                    echo "Node.js版本低于14，安装最新LTS版本..."
                    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
                    apt install -y nodejs
                fi
            fi
            
            echo "✅ 基础依赖安装完成"
            ;;
        1) # 跳过
            echo "跳过软件包安装步骤"
            ;;
        2) # 显示命令
            echo "要手动安装必要的软件包，请执行以下命令:"
            echo "# 更新软件包列表"
            echo "apt update"
            echo ""
            echo "# 安装基本工具"
            echo "apt install -y curl wget git"
            echo ""
            echo "# 安装Python3"
            echo "apt install -y python3 python3-pip python3-venv"
            echo ""
            echo "# 安装Node.js"
            echo "apt install -y nodejs npm"
            echo ""
            echo "# 如果Node.js版本低于14，升级到最新LTS版本"
            echo "curl -fsSL https://deb.nodesource.com/setup_18.x | bash -"
            echo "apt install -y nodejs"
            read -p "按回车键继续..." dummy
            ;;
    esac
}

# 安装Python依赖
install_python_dependencies() {
    echo "检查Python依赖..."
    
    # 检查Python是否安装
    if ! command -v python3 &> /dev/null; then
        local check_result="⚠️ Python3未安装，无法安装Python依赖"
        
        # 询问用户
        ask_user "安装Python依赖" "$check_result"
        local user_choice=$?
        
        case $user_choice in
            0|1) # 自动执行或跳过
                echo "跳过Python依赖安装步骤（Python3未安装）"
                return 0
                ;;
            2) # 显示命令
                echo "要安装Python3和依赖，请执行以下操作:"
                echo "1. 安装Python3: apt install -y python3 python3-pip python3-venv"
                echo "2. 创建虚拟环境: cd $PROJECT_ROOT/backend && python3 -m venv venv"
                echo "3. 激活虚拟环境: source venv/bin/activate"
                echo "4. 安装依赖: pip install -r requirements.txt"
                echo "5. 退出虚拟环境: deactivate"
                read -p "按回车键继续..." dummy
                return 0
                ;;
        esac
    fi
    
    # 检查虚拟环境和依赖
    if [ -d "$PROJECT_ROOT/backend/venv" ]; then
        local check_result="✅ Python虚拟环境已存在，可能需要更新依赖"
    else
        local check_result="⚠️ Python虚拟环境不存在，需要创建并安装依赖"
    fi
    
    # 询问用户
    ask_user "安装Python依赖" "$check_result"
    local user_choice=$?
    
    case $user_choice in
        0) # 自动执行
            echo "安装Python依赖..."
            
            cd "$PROJECT_ROOT/backend"
            
            # 检查是否已存在venv
            if [ ! -d "venv" ]; then
                echo "创建Python虚拟环境..."
                python3 -m venv venv
            fi
            
            # 激活虚拟环境
            source venv/bin/activate
            
            # 安装依赖
            echo "安装Python包依赖..."
            pip install -r requirements.txt
            
            # 退出虚拟环境
            deactivate
            
            cd "$PROJECT_ROOT"
            echo "✅ Python依赖安装完成"
            ;;
        1) # 跳过
            echo "跳过Python依赖安装步骤"
            ;;
        2) # 显示命令
            echo "要手动安装Python依赖，请执行以下命令:"
            echo "cd $PROJECT_ROOT/backend"
            echo "# 创建虚拟环境（如果不存在）"
            echo "python3 -m venv venv"
            echo "# 激活虚拟环境"
            echo "source venv/bin/activate"
            echo "# 安装依赖"
            echo "pip install -r requirements.txt"
            echo "# 退出虚拟环境"
            echo "deactivate"
            echo "cd $PROJECT_ROOT"
            read -p "按回车键继续..." dummy
            ;;
    esac
}

# 安装Node.js依赖和构建前端
install_nodejs_dependencies() {
    echo "检查Node.js依赖..."
    
    # 检查Node.js是否安装
    if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
        local check_result="⚠️ Node.js或npm未安装，无法安装前端依赖"
        
        # 询问用户
        ask_user "安装Node.js依赖并构建前端" "$check_result"
        local user_choice=$?
        
        case $user_choice in
            0|1) # 自动执行或跳过
                echo "跳过Node.js依赖安装步骤（Node.js或npm未安装）"
                return 0
                ;;
            2) # 显示命令
                echo "要安装Node.js和前端依赖，请执行以下操作:"
                echo "1. 安装Node.js: apt install -y nodejs npm"
                echo "2. 安装前端依赖: cd $PROJECT_ROOT/frontend && npm install"
                echo "3. 构建前端: npm run build"
                read -p "按回车键继续..." dummy
                return 0
                ;;
        esac
    fi
    
    # 检查node_modules目录
    if [ -d "$PROJECT_ROOT/frontend/node_modules" ]; then
        local check_result="✅ 前端依赖已安装，可能需要更新"
    else
        local check_result="⚠️ 前端依赖未安装，需要安装并构建"
    fi
    
    # 询问用户
    ask_user "安装Node.js依赖并构建前端" "$check_result"
    local user_choice=$?
    
    case $user_choice in
        0) # 自动执行
            echo "安装Node.js依赖并构建前端..."
            
            cd "$PROJECT_ROOT/frontend"
            
            # 安装依赖
            echo "安装npm包依赖..."
            npm install
            
            # 构建前端
            echo "构建前端..."
            npm run build
            
            cd "$PROJECT_ROOT"
            echo "✅ 前端构建完成"
            ;;
        1) # 跳过
            echo "跳过Node.js依赖安装和前端构建步骤"
            ;;
        2) # 显示命令
            echo "要手动安装Node.js依赖并构建前端，请执行以下命令:"
            echo "cd $PROJECT_ROOT/frontend"
            echo "# 安装依赖"
            echo "npm install"
            echo "# 构建前端"
            echo "npm run build"
            echo "cd $PROJECT_ROOT"
            read -p "按回车键继续..." dummy
            ;;
    esac
}

# 主函数
main() {
    echo "==============================================="
    echo "      开始执行编译环境准备脚本"
    echo "==============================================="
    echo "此脚本将引导您完成以下步骤:"
    echo "1. 创建必要的目录结构"
    echo "2. 配置APT国内源"
    echo "3. 配置pip国内源"
    echo "4. 安装必要的软件包"
    echo "5. 配置npm国内源"
    echo "6. 安装Python依赖"
    echo "7. 安装Node.js依赖并构建前端"
    echo ""
    echo "对于每一步，您可以选择:"
    echo "- 自动执行该步骤"
    echo "- 跳过该步骤"
    echo "- 查看手动执行的命令"
    echo "==============================================="
    read -p "按回车键开始..." dummy
    
    create_directories
    setup_apt_mirrors
    setup_pip_mirrors
    install_dependencies
    setup_npm_mirrors
    install_python_dependencies
    install_nodejs_dependencies
    
    echo "==============================================="
    echo "      编译环境准备完成！"
    echo "==============================================="
    echo "现在您可以运行 sudo bash build/scripts/prepare-docker.sh 来准备Docker环境"
}

# 执行主函数
main 