import os
import json
import time
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

from utils import load_config, save_config, setup_logger
from updater import run_updater
from geoip_updater import run_geo_updater

# 初始化日志
logger = setup_logger("app.log")
logger.info("=" * 50)
logger.info("Mihomo自动更新服务启动")
logger.info("日志系统初始化完成 - 最大10MB，最多10个备份文件")
logger.info("=" * 50)

# 加载配置
# 配置文件位置优先从环境变量获取，如未设置则使用默认路径
config_dir = os.environ.get('CONFIG_DIR', '/config')
config_path = os.path.join(config_dir, "config.yaml")
# 历史记录文件路径
history_path = os.path.join(config_dir, "task_history.json")

# 检查配置目录是否存在
if not os.path.exists(config_dir):
    logger.info(f"配置目录 {config_dir} 不存在，尝试创建")
    try:
        os.makedirs(config_dir, exist_ok=True)
    except Exception as e:
        logger.error(f"创建配置目录失败: {e}")

# 如果配置文件不存在，先创建一个默认配置
if not os.path.exists(config_path):
    # 检查临时目录中是否有默认配置
    tmp_config_path = "/tmp/config.yaml"
    if os.path.exists(tmp_config_path):
        logger.info(f"正在从 {tmp_config_path} 复制默认配置到 {config_path}")
        try:
            import shutil
            shutil.copy(tmp_config_path, config_path)
        except Exception as e:
            logger.error(f"复制默认配置失败: {e}")

logger.info(f"尝试加载配置文件: {config_path}")
config = load_config(config_path)

if not config:
    logger.error("无法加载配置文件，使用默认配置")
    config = {
        "fetch_url": "https://mahoushaojiu.ruan.day/sub/0a97acae18076274/clash",
        "fetch_interval": 3600,
        "geoip_fetch_interval": 86400,
        "mihomo_config_path": "/etc/mihomo/config.yaml",
        "backup_dir": "/etc/mihomo/data/backups",
        "geoip_url": "https://github.com/MetaCubeX/meta-rules-dat/releases/latest/download/geoip.dat",
        "geosite_url": "https://github.com/MetaCubeX/meta-rules-dat/releases/latest/download/geosite.dat",
        "mmdb_url": "https://github.com/MetaCubeX/meta-rules-dat/releases/latest/download/country.mmdb",
        "geoip_path": "/etc/mihomo/geoip.dat",
        "geosite_path": "/etc/mihomo/geosite.dat",
        "mmdb_path": "/etc/mihomo/country.mmdb",
        "yacd_url": "http://192.168.3.110:8080",
        "clash_api_url": "http://192.168.3.110:9097",
        "web_port": 5000
    }
    save_config(config, config_path)
    logger.info("使用默认配置初始化配置文件")
else:
    logger.info("成功加载配置文件")

    # 确保backup_dir指向持久化目录
    if config.get('backup_dir') == '/etc/mihomo/backups':
        config['backup_dir'] = '/etc/mihomo/data/backups'
        logger.info(f"更新备份目录为持久化目录: {config['backup_dir']}")
        save_config(config, config_path)

# 确保备份目录存在
backup_dir = config.get('backup_dir', '/etc/mihomo/data/backups')
os.makedirs(backup_dir, exist_ok=True)
logger.info(f"确保备份目录存在: {backup_dir}")

# 初始化Flask应用
app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend/dist"),
            static_url_path='')
CORS(app)  # 启用CORS
logger.info(f"Flask应用初始化完成，CORS已启用")

# 从文件加载任务执行历史记录
def load_task_history():
    """从JSON文件加载任务执行历史"""
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载任务历史记录失败: {e}")
    return []

# 保存任务执行历史记录到文件
def save_task_history(history):
    """保存任务执行历史到JSON文件"""
    try:
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"保存任务历史记录失败: {e}")
        return False

# 存储任务执行结果的列表
task_results = load_task_history()
logger.info(f"加载了 {len(task_results)} 条历史任务记录")

# 记录任务执行结果
def log_task_result(task_name, success, message=None):
    """记录任务执行结果到全局列表并持久化存储"""
    global task_results
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task": task_name,
        "success": success,
        "message": message or ("成功" if success else "失败")
    }
    task_results.append(result)
    # 只保留最新的50条记录
    if len(task_results) > 50:
        task_results = task_results[-50:]
    # 持久化保存
    save_task_history(task_results)

# 定时更新Mihomo配置的任务
def update_mihomo_config_job():
    """定时更新Mihomo配置任务"""
    logger.info("开始执行Mihomo配置更新任务")
    try:
        success = run_updater()
        log_task_result("Mihomo配置更新", success)
        return success
    except Exception as e:
        logger.error(f"Mihomo配置更新任务失败: {e}")
        log_task_result("Mihomo配置更新", False, str(e))
        return False

# 定时更新GeoIP数据的任务
def update_geoip_job():
    """定时更新GeoIP数据任务"""
    logger.info("开始执行GeoIP数据更新任务")
    try:
        success = run_geo_updater()
        log_task_result("GeoIP数据更新", success)
        return success
    except Exception as e:
        logger.error(f"GeoIP数据更新任务失败: {e}")
        log_task_result("GeoIP数据更新", False, str(e))
        return False

# 初始化定时任务调度器
scheduler = BackgroundScheduler()
logger.info("初始化定时任务调度器")

# 添加Mihomo配置更新任务
scheduler.add_job(
    update_mihomo_config_job,
    IntervalTrigger(seconds=config.get('fetch_interval', 3600)),
    id='update_mihomo_config',
    replace_existing=True
)
logger.info(f"添加Mihomo配置更新任务，间隔: {config.get('fetch_interval', 3600)}秒")

# 添加GeoIP数据更新任务
scheduler.add_job(
    update_geoip_job,
    IntervalTrigger(seconds=config.get('geoip_fetch_interval', 86400)),
    id='update_geoip',
    replace_existing=True
)
logger.info(f"添加GeoIP数据更新任务，间隔: {config.get('geoip_fetch_interval', 86400)}秒")

# 启动调度器
scheduler.start()
logger.info("定时任务调度器已启动")

# 主页路由
@app.route('/')
def index():
    """返回前端静态文件"""
    return send_from_directory(app.static_folder, 'index.html')

# API路由 - 获取配置
@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    try:
        config = load_config(config_path)
        return jsonify({"success": True, "data": config})
    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# API路由 - 更新配置
@app.route('/api/config', methods=['POST'])
def update_config():
    """更新配置"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "没有提供配置数据"}), 400
        
        current_config = load_config(config_path)
        
        # 更新配置项
        for key, value in data.items():
            current_config[key] = value
        
        # 保存更新后的配置
        if save_config(current_config, config_path):
            # 更新调度器中的任务间隔
            if 'fetch_interval' in data:
                scheduler.reschedule_job(
                    'update_mihomo_config', 
                    trigger=IntervalTrigger(seconds=data['fetch_interval'])
                )
                logger.info(f"更新Mihomo配置更新间隔为: {data['fetch_interval']}秒")
            
            if 'geoip_fetch_interval' in data:
                scheduler.reschedule_job(
                    'update_geoip', 
                    trigger=IntervalTrigger(seconds=data['geoip_fetch_interval'])
                )
                logger.info(f"更新GeoIP数据更新间隔为: {data['geoip_fetch_interval']}秒")
                
            return jsonify({"success": True, "message": "配置已更新"})
        else:
            return jsonify({"success": False, "message": "保存配置失败"}), 500
    except Exception as e:
        logger.error(f"更新配置失败: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# API路由 - 手动触发Mihomo配置更新
@app.route('/api/update/mihomo', methods=['POST'])
def manual_update_mihomo():
    """手动触发Mihomo配置更新"""
    logger.info("手动触发Mihomo配置更新")
    success = update_mihomo_config_job()
    return jsonify({"success": success, "message": "Mihomo配置更新" + ("成功" if success else "失败")})

# API路由 - 从本地YAML文件导入配置
@app.route('/api/import/local', methods=['POST'])
def import_local_yaml():
    """从本地YAML文件导入配置"""
    try:
        if 'file' not in request.files:
            logger.error("未提供文件")
            return jsonify({"success": False, "message": "未提供文件"}), 400
        
        yaml_file = request.files['file']
        if yaml_file.filename == '':
            logger.error("未选择文件")
            return jsonify({"success": False, "message": "未选择文件"}), 400
        
        # 从上传的文件读取YAML内容
        yaml_content = yaml_file.read().decode('utf-8')
        logger.info(f"已上传本地YAML文件，大小: {len(yaml_content)}字节")
        
        # 解析YAML内容
        from updater import MihomoUpdater
        updater = MihomoUpdater()
        success = updater.update_with_yaml_content(yaml_content)
        
        if success:
            log_task_result("从本地文件导入配置", True)
            return jsonify({"success": True, "message": "从本地文件导入配置成功"})
        else:
            log_task_result("从本地文件导入配置", False, "导入失败")
            return jsonify({"success": False, "message": "从本地文件导入配置失败"}), 500
            
    except Exception as e:
        logger.error(f"从本地文件导入配置失败: {e}")
        log_task_result("从本地文件导入配置", False, str(e))
        return jsonify({"success": False, "message": str(e)}), 500

# API路由 - 手动触发GeoIP数据更新
@app.route('/api/update/geoip', methods=['POST'])
def manual_update_geoip():
    """手动触发GeoIP数据更新"""
    logger.info("手动触发GeoIP数据更新")
    success = update_geoip_job()
    return jsonify({"success": success, "message": "GeoIP数据更新" + ("成功" if success else "失败")})

# API路由 - 获取任务执行历史
@app.route('/api/history', methods=['GET'])
def get_task_history():
    """获取任务执行历史"""
    return jsonify({"success": True, "data": task_results})

# 健康检查路由
@app.route('/health')
def health_check():
    """健康检查接口"""
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # 启动时立即执行一次更新任务
    logger.info("服务启动，执行初始更新任务")
    update_mihomo_config_job()
    update_geoip_job()
    
    # 启动Flask应用
    port = config.get('web_port', 5000)
    logger.info(f"Mihomo自动更新服务已启动，监听端口: {port}")
    app.run(host='0.0.0.0', port=port) 