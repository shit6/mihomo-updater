import os
import requests
import yaml
import logging
import subprocess
import time
from utils import load_config, save_config, create_backup, parse_yaml, merge_configs, setup_logger

# 初始化日志
logger = setup_logger("updater.log")
logger.info("Mihomo配置更新器初始化")

class MihomoUpdater:
    def __init__(self, config_path="config.yaml"):
        """初始化Mihomo配置更新器"""
        self.config_path = config_path
        self.config = load_config(config_path)
        if not self.config:
            logger.error("无法加载配置文件")
            raise ValueError("配置文件加载失败")
        
        logger.info("Mihomo配置更新器配置加载成功")
        
        # 设置用户代理
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # 确保备份目录存在
        backup_dir = self.config.get('backup_dir', '/etc/mihomo/backups')
        os.makedirs(backup_dir, exist_ok=True)
        logger.info(f"备份目录确认: {backup_dir}")

    def fetch_remote_config(self):
        """从远程URL获取配置文件"""
        try:
            url = self.config['fetch_url']
            logger.info(f"正在从 {url} 获取远程配置")
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            config_content = response.text
            logger.info(f"成功获取远程配置，大小: {len(config_content)} 字节")
            return config_content
        except Exception as e:
            logger.error(f"获取远程配置失败: {e}")
            return None

    def update_with_yaml_content(self, yaml_content):
        """使用提供的YAML内容更新Mihomo配置文件"""
        try:
            logger.info("开始使用提供的YAML内容更新Mihomo配置")
            
            # 解析提供的YAML内容
            logger.info("正在解析提供的YAML内容")
            remote_config = parse_yaml(yaml_content)
            if not remote_config:
                logger.error("解析提供的YAML内容失败")
                return False
            
            # 读取当前的mihomo配置
            mihomo_config_path = self.config['mihomo_config_path']
            logger.info(f"正在读取当前Mihomo配置: {mihomo_config_path}")
            
            if not os.path.exists(mihomo_config_path):
                logger.error(f"Mihomo配置文件不存在: {mihomo_config_path}")
                return False
            
            # 备份当前配置
            logger.info("正在备份当前配置文件")
            backup_path = create_backup(
                mihomo_config_path, 
                self.config['backup_dir']
            )
            if not backup_path:
                logger.error("备份配置文件失败")
                return False
            
            logger.info(f"已备份原配置文件到: {backup_path}")
            
            # 读取和解析原始配置
            logger.info("正在读取和解析原始配置文件")
            with open(mihomo_config_path, 'r', encoding='utf-8') as f:
                original_config_content = f.read()
            
            original_config = parse_yaml(original_config_content)
            if not original_config:
                logger.error("解析原始配置失败")
                return False
            
            # 合并配置，保留原始配置中的关键部分，只更新proxies, proxy-groups, rules
            logger.info("正在合并配置文件")
            merged_config = merge_configs(original_config, remote_config)
            
            # 保存合并后的配置
            logger.info(f"正在保存合并后的配置到: {mihomo_config_path}")
            with open(mihomo_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(merged_config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"成功更新Mihomo配置文件: {mihomo_config_path}")
            
            # 检查是否需要重启mihomo服务
            logger.info("配置更新完成，准备重启服务")
            self.restart_mihomo_service()
            
            return True
        except Exception as e:
            logger.error(f"使用提供的YAML内容更新Mihomo配置失败: {e}")
            return False

    def update_mihomo_config(self):
        """更新Mihomo配置文件"""
        try:
            # 获取远程配置
            logger.info("开始更新Mihomo配置")
            remote_config_content = self.fetch_remote_config()
            if not remote_config_content:
                logger.error("无法获取远程配置，更新失败")
                return False
            
            # 使用获取的YAML内容更新配置
            return self.update_with_yaml_content(remote_config_content)
        except Exception as e:
            logger.error(f"更新Mihomo配置失败: {e}")
            return False

    def restart_mihomo_service(self):
        """重启Mihomo服务"""
        try:
            # 根据实际情况使用systemctl或其他方式重启服务
            logger.info("尝试重启Mihomo服务...")
            subprocess.run(['systemctl', 'restart', 'mihomo.service'], check=True)
            logger.info("Mihomo服务重启成功")
            return True
        except Exception as e:
            logger.error(f"重启Mihomo服务失败: {e}")
            return False

def run_updater():
    """运行配置更新器"""
    try:
        logger.info("=" * 50)
        logger.info("启动Mihomo配置更新")
        logger.info("=" * 50)
        
        updater = MihomoUpdater()
        success = updater.update_mihomo_config()
        
        if success:
            logger.info("Mihomo配置更新成功")
        else:
            logger.error("Mihomo配置更新失败")
            
        return success
    except Exception as e:
        logger.error(f"配置更新器运行失败: {e}")
        return False

if __name__ == "__main__":
    # 直接运行时立即更新配置
    success = run_updater()
    if success:
        logger.info("Mihomo配置更新成功")
    else:
        logger.error("Mihomo配置更新失败") 