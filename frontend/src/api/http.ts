import axios, { AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { ApiResponse } from '@/types'

// 创建axios实例
const instance = axios.create({
  timeout: 15000, // 请求超时时间15秒
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    return config
  },
  (error: AxiosError): Promise<AxiosError> => {
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  (response: AxiosResponse): any => {
    const res = response.data
    return res
  },
  (error: AxiosError): Promise<any> => {
    let message = '请求失败'
    if (error.response) {
      switch (error.response.status) {
        case 404:
          message = '请求的资源不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = (error.response.data as any)?.message || `请求错误(${error.response.status})`
      }
    } else if (error.request) {
      message = '服务器无响应，请检查网络连接'
    }
    return Promise.reject(new Error(message))
  }
)

// GET请求
export function get<T = any>(url: string, params?: any): Promise<ApiResponse<T>> {
  return instance.get(url, { params })
}

// POST请求
export function post<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
  return instance.post(url, data)
}

// PUT请求
export function put<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
  return instance.put(url, data)
}

// DELETE请求
export function del<T = any>(url: string, params?: any): Promise<ApiResponse<T>> {
  return instance.delete(url, { params })
}

export default instance 