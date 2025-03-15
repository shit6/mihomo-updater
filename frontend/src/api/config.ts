import { get, post } from './http'
import { Config, ApiResponse } from '@/types'

// 获取当前配置
export function getConfig(): Promise<ApiResponse<Config>> {
  return get<Config>('/api/config')
}

// 更新配置
export function updateConfig(config: Partial<Config>): Promise<ApiResponse<void>> {
  return post<void>('/api/config', config)
} 