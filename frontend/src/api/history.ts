import { get } from './http'
import { TaskHistory, ApiResponse } from '@/types'

// 获取任务执行历史
export function getTaskHistory(): Promise<ApiResponse<TaskHistory[]>> {
  return get<TaskHistory[]>('/api/history')
} 