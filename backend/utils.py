import os
import yaml
import logging
from logging.handlers import RotatingFileHandler
import datetime
import shutil
from pathlib import Path

# 配置日志
def setup_logger(log_file="mihomo_updater.log"):
    """设置日志记录器"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_path = os.path.join(log_dir, log_file)
    
    # 创建logger
    logger = logging.getLogger("mihomo-updater")
    logger.setLevel(logging.INFO)
    
    # 清除已有handlers以防重复
    if logger.handlers:
        logger.handlers.clear()
    
    # 创建RotatingFileHandler
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    
    # 配置formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # 添加到logger
    logger.addHandler(file_handler)
    
    # 添加控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# 加载配置文件
def load_config(config_path="config.yaml"):
    """从YAML文件加载配置"""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger = logging.getLogger("mihomo-updater")
        logger.error(f"加载配置文件失败: {e}")
        return None

# 保存配置文件
def save_config(config, config_path="config.yaml"):
    """将配置保存到YAML文件"""
    try:
        # 确保配置文件目录存在
        config_dir = os.path.dirname(config_path)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
            
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        logger = logging.getLogger("mihomo-updater")
        logger.error(f"保存配置文件失败: {e}")
        return False

# 创建备份
def create_backup(file_path, backup_dir, max_backups=10):
    """创建文件备份，并管理备份数量"""
    logger = logging.getLogger("mihomo-updater")
    
    # 检查原文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"要备份的文件不存在: {file_path}")
        return None
    
    # 确保备份目录存在
    os.makedirs(backup_dir, exist_ok=True)
    
    # 创建带时间戳的备份文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{os.path.basename(file_path)}.{timestamp}.bak"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # 复制文件
    try:
        shutil.copy2(file_path, backup_path)
        logger.info(f"成功创建备份: {backup_path}")
        
        # 管理备份数量
        backup_files = sorted([
            os.path.join(backup_dir, f) for f in os.listdir(backup_dir)
            if f.startswith(os.path.basename(file_path)) and f.endswith(".bak")
        ])
        
        # 如果备份数量超过限制，删除最旧的备份
        if len(backup_files) > max_backups:
            files_to_delete = backup_files[:-max_backups]
            for old_file in files_to_delete:
                os.remove(old_file)
                logger.info(f"删除旧备份: {old_file}")
        
        return backup_path
    except Exception as e:
        logger.error(f"创建备份失败: {e}")
        return None

# 解析YAML配置文件
def parse_yaml(yaml_content):
    """解析YAML内容为Python对象"""
    try:
        return yaml.safe_load(yaml_content)
    except Exception as e:
        logger = logging.getLogger("mihomo-updater")
        logger.error(f"解析YAML内容失败: {e}")
        return None

# 合并配置文件
def merge_configs(original_config, new_config):
    """合并原始配置和新配置，只替换proxies, proxy-groups, rules部分"""
    # 保留原始配置
    merged_config = original_config.copy()
    
    # 更新特定部分
    for key in ['proxies', 'proxy-groups', 'rules']:
        if key in new_config:
            merged_config[key] = new_config[key]
    
    return merged_config 