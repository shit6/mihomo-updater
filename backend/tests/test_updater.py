import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
import yaml
import pytest
import requests
import shutil

# 添加父目录到系统路径，以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入被测试的模块
from updater import MihomoUpdater, run_updater
from utils import load_config, parse_yaml, merge_configs

# 获取实际配置文件路径
REAL_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yaml')

# 测试文件夹路径
TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
TEST_MIHOMO_CONFIG_PATH = os.path.join(TEST_DIR, 'mihomo_config.yaml')
TEST_BACKUP_DIR = os.path.join(TEST_DIR, 'backups')

class TestMihomoUpdater(unittest.TestCase):
    """测试 MihomoUpdater 类，使用真实配置文件"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化，只执行一次"""
        # 确保测试目录存在
        os.makedirs(TEST_DIR, exist_ok=True)
        os.makedirs(TEST_BACKUP_DIR, exist_ok=True)
    
    def setUp(self):
        """每个测试前的设置"""
        # 确保真实配置文件存在
        self.assertTrue(os.path.exists(REAL_CONFIG_PATH), f"配置文件不存在: {REAL_CONFIG_PATH}")
        
        # 加载真实配置
        self.real_config = load_config(REAL_CONFIG_PATH)
        self.assertIsNotNone(self.real_config, "无法加载配置文件")
        
        # 创建一个示例mihomo配置文件用于测试
        sample_mihomo_config = {
            "port": 7890,
            "mode": "rule",
            "log-level": "info",
            "proxies": [{"name": "test_proxy", "type": "http", "server": "example.com", "port": 8080}],
            "proxy-groups": [{"name": "PROXY", "type": "select", "proxies": ["test_proxy"]}],
            "rules": ["DOMAIN-SUFFIX,google.com,PROXY", "MATCH,DIRECT"]
        }
        
        with open(TEST_MIHOMO_CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(sample_mihomo_config, f, default_flow_style=False, allow_unicode=True)
    
    def tearDown(self):
        """每个测试结束后清理"""
        # 清理备份文件
        for f in os.listdir(TEST_BACKUP_DIR):
            os.remove(os.path.join(TEST_BACKUP_DIR, f))
    
    def test_init_with_real_config(self):
        """使用真实配置文件初始化更新器"""
        with patch('updater.load_config') as mock_load_config:
            # 修改返回的配置，使其使用测试目录
            test_config = self.real_config.copy()
            test_config['mihomo_config_path'] = TEST_MIHOMO_CONFIG_PATH
            test_config['backup_dir'] = TEST_BACKUP_DIR
            mock_load_config.return_value = test_config
            
            # 模拟目录创建
            with patch('os.makedirs') as mock_makedirs:
                updater = MihomoUpdater(REAL_CONFIG_PATH)
                
                # 验证
                self.assertEqual(updater.config['fetch_url'], self.real_config['fetch_url'])
                self.assertEqual(updater.config['mihomo_config_path'], TEST_MIHOMO_CONFIG_PATH)
                self.assertEqual(updater.config['backup_dir'], TEST_BACKUP_DIR)
    
    def test_fetch_remote_config_with_real_url(self):
        """使用真实URL测试获取远程配置（模拟响应）"""
        with patch('updater.load_config') as mock_load_config:
            # 修改返回的配置，使其使用测试目录
            test_config = self.real_config.copy()
            test_config['mihomo_config_path'] = TEST_MIHOMO_CONFIG_PATH
            test_config['backup_dir'] = TEST_BACKUP_DIR
            mock_load_config.return_value = test_config
            
            # 模拟网络请求
            with patch('requests.get') as mock_get:
                # 模拟请求响应
                mock_response = MagicMock()
                mock_response.text = 'remote config content'
                mock_response.raise_for_status = MagicMock()
                mock_get.return_value = mock_response
                
                # 初始化更新器并调用方法
                updater = MihomoUpdater(REAL_CONFIG_PATH)
                result = updater.fetch_remote_config()
                
                # 验证
                self.assertEqual(result, 'remote config content')
                # 验证使用了真实URL
                mock_get.assert_called_once_with(
                    self.real_config['fetch_url'],
                    headers=updater.headers,
                    timeout=30
                )
    
    # @pytest.mark.skip(reason="可能会发送真实网络请求，根据需要启用")
    def test_fetch_remote_config_actual_request(self):
        """发送真实网络请求获取远程配置"""
        with patch('updater.load_config') as mock_load_config:
            # 修改返回的配置，使其使用测试目录
            test_config = self.real_config.copy()
            test_config['mihomo_config_path'] = TEST_MIHOMO_CONFIG_PATH
            test_config['backup_dir'] = TEST_BACKUP_DIR
            mock_load_config.return_value = test_config
            
            updater = MihomoUpdater(REAL_CONFIG_PATH)
            result = updater.fetch_remote_config()
            
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0)
            
            # 可选：验证返回的内容是有效的YAML
            parsed = parse_yaml(result)
            self.assertIsNotNone(parsed)
    
    def test_create_backup_with_real_files(self):
        """测试实际创建备份文件"""
        # 直接导入create_backup函数
        from utils import create_backup
        
        # 验证源文件存在
        self.assertTrue(os.path.exists(TEST_MIHOMO_CONFIG_PATH))
        
        # 创建备份
        backup_path = create_backup(
            TEST_MIHOMO_CONFIG_PATH,
            TEST_BACKUP_DIR
        )
        
        # 验证
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))
        
        # 验证备份内容
        with open(TEST_MIHOMO_CONFIG_PATH, 'r', encoding='utf-8') as original:
            original_content = original.read()
        
        with open(backup_path, 'r', encoding='utf-8') as backup:
            backup_content = backup.read()
        
        self.assertEqual(original_content, backup_content)
    
    def test_merge_configs_with_real_format(self):
        """测试合并配置，使用真实格式的配置"""
        # 创建与真实格式类似的配置
        original_config = {
            "port": 7890,
            "mode": "rule",
            "log-level": "info",
            "proxies": [{"name": "original_proxy", "type": "http", "server": "example.com", "port": 8080}],
            "proxy-groups": [{"name": "ORIGINAL", "type": "select", "proxies": ["original_proxy"]}],
            "rules": ["DOMAIN-SUFFIX,example.com,ORIGINAL", "MATCH,DIRECT"]
        }
        
        new_config = {
            "port": 7891,  # 不同的端口
            "proxies": [{"name": "new_proxy", "type": "http", "server": "example.org", "port": 8081}],
            "proxy-groups": [{"name": "NEW", "type": "select", "proxies": ["new_proxy"]}],
            "rules": ["DOMAIN-SUFFIX,google.com,NEW", "MATCH,DIRECT"]
        }
        
        # 合并配置
        merged_config = merge_configs(original_config, new_config)
        
        # 验证
        # 端口应该保持原样
        self.assertEqual(merged_config["port"], original_config["port"])
        # 模式应该保持原样
        self.assertEqual(merged_config["mode"], original_config["mode"])
        # 代理已替换
        self.assertEqual(merged_config["proxies"], new_config["proxies"])
        # 代理组已替换
        self.assertEqual(merged_config["proxy-groups"], new_config["proxy-groups"])
        # 规则已替换
        self.assertEqual(merged_config["rules"], new_config["rules"])
    
    def test_update_mihomo_config_with_real_files(self):
        """测试更新Mihomo配置"""
        with patch('updater.load_config') as mock_load_config:
            # 修改返回的配置，使其使用测试目录
            test_config = self.real_config.copy()
            test_config['mihomo_config_path'] = TEST_MIHOMO_CONFIG_PATH
            test_config['backup_dir'] = TEST_BACKUP_DIR
            mock_load_config.return_value = test_config
            
            # 准备模拟的远程配置内容
            mock_remote_content = yaml.dump({
                "port": 7891,
                "proxies": [{"name": "updated_proxy", "type": "http", "server": "test.com", "port": 443}],
                "proxy-groups": [{"name": "UPDATED", "type": "select", "proxies": ["updated_proxy"]}],
                "rules": ["DOMAIN-SUFFIX,updated.com,UPDATED", "MATCH,DIRECT"]
            })
            
            # 获取原始配置内容
            with open(TEST_MIHOMO_CONFIG_PATH, 'r', encoding='utf-8') as f:
                original_content = f.read()
            original_config = yaml.safe_load(original_content)
            
            # 模拟fetch_remote_config和restart_mihomo_service
            with patch.object(MihomoUpdater, 'fetch_remote_config', return_value=mock_remote_content), \
                patch.object(MihomoUpdater, 'restart_mihomo_service', return_value=True):
                
                # 执行更新
                updater = MihomoUpdater(REAL_CONFIG_PATH)
                result = updater.update_mihomo_config()
                
                # 验证
                self.assertTrue(result)
                
                # 验证配置文件已更新
                with open(TEST_MIHOMO_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    updated_content = f.read()
                updated_config = yaml.safe_load(updated_content)
                
                # 端口应保持原样
                self.assertEqual(updated_config['port'], original_config['port'])
                
                # 代理已更新
                self.assertEqual(updated_config['proxies'][0]['name'], "updated_proxy")
                
                # 代理组已更新
                self.assertEqual(updated_config['proxy-groups'][0]['name'], "UPDATED")
                
                # 规则已更新
                self.assertTrue("DOMAIN-SUFFIX,updated.com,UPDATED" in updated_config['rules'])
    
    def test_restart_mihomo_service_mocked(self):
        """测试重启Mihomo服务（模拟执行）"""
        with patch('updater.load_config') as mock_load_config:
            # 修改返回的配置，使其使用测试目录
            test_config = self.real_config.copy()
            test_config['mihomo_config_path'] = TEST_MIHOMO_CONFIG_PATH
            test_config['backup_dir'] = TEST_BACKUP_DIR
            mock_load_config.return_value = test_config
            
            with patch('subprocess.run') as mock_run:
                updater = MihomoUpdater(REAL_CONFIG_PATH)
                result = updater.restart_mihomo_service()
                
                # 验证
                self.assertTrue(result)
                mock_run.assert_called_once_with(['systemctl', 'restart', 'mihomo.service'], check=True)
    
    def test_run_updater_integration(self):
        """集成测试运行更新器（模拟依赖）"""
        with patch('updater.load_config') as mock_load_config:
            # 修改返回的配置，使其使用测试目录
            test_config = self.real_config.copy()
            test_config['mihomo_config_path'] = TEST_MIHOMO_CONFIG_PATH
            test_config['backup_dir'] = TEST_BACKUP_DIR
            mock_load_config.return_value = test_config
            
            # 模拟更新
            with patch.object(MihomoUpdater, 'fetch_remote_config', return_value='remote content'), \
                patch.object(MihomoUpdater, 'restart_mihomo_service', return_value=True), \
                patch('subprocess.run'):
                
                # 运行更新器
                result = run_updater()
                
                # 验证
                self.assertTrue(result)

if __name__ == '__main__':
    unittest.main() 