#!/bin/bash
set -e

CONFIG_DIR="/config"
CONFIG_FILE="$CONFIG_DIR/config.yaml"
DEFAULT_CONFIG="/tmp/config.yaml"
MIHOMO_DATA_DIR="/etc/mihomo/data"
MIHOMO_BACKUP_DIR="$MIHOMO_DATA_DIR/backups"

# 创建配置目录（如果不存在）
mkdir -p $CONFIG_DIR

# 创建logs目录（如果不存在）
mkdir -p /app/logs

# 创建mihomo数据目录和备份目录（如果不存在）
mkdir -p $MIHOMO_DATA_DIR
mkdir -p $MIHOMO_BACKUP_DIR

# 如果目录是空的，创建必要的子目录
if [ ! "$(ls -A $CONFIG_DIR)" ]; then
    echo "配置目录为空，创建必要的子目录结构..."
    mkdir -p $CONFIG_DIR
fi

# 检查配置文件是否存在，如果不存在则复制默认配置
if [ ! -f "$CONFIG_FILE" ]; then
    echo "找不到配置文件，正在复制默认配置..."
    cp $DEFAULT_CONFIG $CONFIG_FILE
    
    # 更新默认配置中的备份目录为持久化目录
    sed -i "s|/etc/mihomo/backups|$MIHOMO_BACKUP_DIR|g" $CONFIG_FILE
    
    echo "默认配置文件已创建: $CONFIG_FILE"
else
    echo "使用现有配置文件: $CONFIG_FILE"
fi

echo "检查任务历史文件..."
HISTORY_FILE="$CONFIG_DIR/task_history.json"
if [ ! -f "$HISTORY_FILE" ]; then
    echo "任务历史文件不存在，创建空文件..."
    echo "[]" > $HISTORY_FILE
    echo "任务历史文件已创建: $HISTORY_FILE"
fi

echo "目录准备完成，启动应用..."
# 启动应用
exec python3 app.py 