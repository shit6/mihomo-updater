// 配置类型定义
export interface Config {
  fetch_url: string;
  fetch_interval: number;
  geoip_fetch_interval: number;
  mihomo_config_path: string;
  backup_dir: string;
  geoip_url: string;
  geosite_url: string;
  mmdb_url: string;
  geoip_path: string;
  geosite_path: string;
  mmdb_path: string;
  yacd_url: string;
  clash_api_url: string;
  web_port: number;
  [key: string]: any;
}

// 历史记录类型定义
export interface TaskHistory {
  timestamp: string;
  task: string;
  success: boolean;
  message: string;
}

// 接口响应类型定义
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
} 