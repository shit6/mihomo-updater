import { post } from './http'
import { ApiResponse } from '@/types'

// 手动触发Mihomo配置更新
export function updateMihomo(): Promise<ApiResponse<void>> {
  return post<void>('/api/update/mihomo')
}

// 手动触发GeoIP数据更新
export function updateGeoIP(): Promise<ApiResponse<void>> {
  return post<void>('/api/update/geoip')
} 