import os
import requests
import logging
import time
from utils import load_config, setup_logger

# 初始化日志
logger = setup_logger("geoip_updater.log")
logger.info("GeoIP更新器初始化")

class GeoIPUpdater:
    def __init__(self, config_path="config.yaml"):
        """初始化GeoIP更新器"""
        self.config_path = config_path
        self.config = load_config(config_path)
        if not self.config:
            logger.error("无法加载配置文件")
            raise ValueError("配置文件加载失败")
        
        logger.info("GeoIP更新器配置加载成功")
        
        # 设置用户代理
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def download_file(self, url, save_path):
        """下载文件并保存到指定路径"""
        try:
            # 创建目录（如果不存在）
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            logger.info(f"准备下载文件: {url} -> {save_path}")
            
            # 检查文件是否存在，如果存在，发送带有If-None-Match头的请求
            etag = None
            if os.path.exists(save_path):
                try:
                    # 发送HEAD请求获取ETag
                    logger.info(f"文件已存在，检查ETag: {save_path}")
                    head_response = requests.head(url, headers=self.headers, timeout=30)
                    if 'ETag' in head_response.headers:
                        etag = head_response.headers['ETag']
                        self.headers['If-None-Match'] = etag
                        logger.info(f"获取到ETag: {etag}")
                except Exception as e:
                    logger.warning(f"获取ETag失败: {e}")
            
            # 下载文件
            logger.info(f"开始下载文件: {url}")
            response = requests.get(url, headers=self.headers, stream=True, timeout=30)
            
            # 如果返回304（未修改），则无需更新
            if response.status_code == 304:
                logger.info(f"文件未修改，无需更新: {save_path}")
                return True
            
            # 检查响应状态
            response.raise_for_status()
            
            # 保存文件
            logger.info(f"开始写入文件: {save_path}")
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"成功下载文件: {save_path}")
            
            # 如果响应包含ETag，保存它
            if 'ETag' in response.headers:
                etag = response.headers['ETag']
                self.headers['If-None-Match'] = etag
                logger.info(f"更新ETag: {etag}")
            
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"下载文件失败 {url}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"保存文件失败 {save_path}: {str(e)}")
            return False

    def update_all_geo_files(self):
        """更新所有GEO文件"""
        success = True
        
        logger.info("开始更新GeoIP数据文件")
        
        # 更新GeoIP数据
        geoip_url = self.config.get('geoip_url', '')
        geoip_path = self.config.get('geoip_path', '/etc/mihomo/geoip.dat')
        logger.info(f"更新GeoIP数据: {geoip_url} -> {geoip_path}")
        
        if not self.download_file(geoip_url, geoip_path):
            logger.error("GeoIP数据更新失败")
            success = False
        else:
            logger.info("GeoIP数据更新成功")
        
        # 更新GeoSite数据
        geosite_url = self.config.get('geosite_url', '')
        geosite_path = self.config.get('geosite_path', '/etc/mihomo/geosite.dat')
        logger.info(f"更新GeoSite数据: {geosite_url} -> {geosite_path}")
        
        if not self.download_file(geosite_url, geosite_path):
            logger.error("GeoSite数据更新失败")
            success = False
        else:
            logger.info("GeoSite数据更新成功")
        
        # 更新MMDB数据
        mmdb_url = self.config.get('mmdb_url', '')
        mmdb_path = self.config.get('mmdb_path', '/etc/mihomo/country.mmdb')
        logger.info(f"更新MMDB数据: {mmdb_url} -> {mmdb_path}")
        
        if not self.download_file(mmdb_url, mmdb_path):
            logger.error("MMDB数据更新失败")
            success = False
        else:
            logger.info("MMDB数据更新成功")
        
        if success:
            logger.info("所有GEO文件更新成功")
        else:
            logger.warning("部分GEO文件更新失败")
        
        return success

def run_geo_updater():
    """运行GeoIP更新器"""
    try:
        logger.info("=" * 50)
        logger.info("启动GeoIP更新")
        logger.info("=" * 50)
        
        updater = GeoIPUpdater()
        success = updater.update_all_geo_files()
        
        if success:
            logger.info("GeoIP更新完成：全部成功")
        else:
            logger.warning("GeoIP更新完成：部分失败")
            
        return success
    except Exception as e:
        logger.error(f"GeoIP更新异常: {e}")
        return False

if __name__ == "__main__":
    # 直接运行时立即更新GeoIP数据
    success = run_geo_updater()
    if success:
        logger.info("GeoIP数据更新成功")
    else:
        logger.error("GeoIP数据更新失败") 