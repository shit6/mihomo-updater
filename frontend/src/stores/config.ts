// 导入必要的工具和功能
import { defineStore } from 'pinia'  // 用于创建数据存储的工具
import { ref } from 'vue'  // Vue框架的核心功能，用于创建响应式数据
import { getConfig, updateConfig } from '@/api/config'  // 从API文件夹导入获取和更新配置的函数
import { Config } from '@/types'  // 从类型定义文件导入配置类型

// 定义一个接口来描述保存操作的结果
interface SaveResult {
  success: boolean;  // 表示操作是否成功，true表示成功，false表示失败
  message: string;   // 操作完成后返回的消息，通常用于显示给用户
}

// 创建一个名为'config'的数据存储
export const useConfigStore = defineStore('config', () => {
  // 创建一个可以存储配置数据的变量，初始值为空对象
  const config = ref<Config | {}>({})
  // 创建一个表示加载状态的变量，初始值为false（未加载）
  const loading = ref<boolean>(false)
  // 创建一个存储错误信息的变量，初始值为null（没有错误）
  const error = ref<string | null>(null)

  // 定义一个异步函数来获取配置
  async function fetchConfig(): Promise<void> {
    // 开始加载，将loading状态设为true
    loading.value = true
    // 清除之前的错误信息
    error.value = null

    try {
      // 调用API获取配置
      const res = await getConfig()
      // 如果API调用成功并且有数据返回
      if (res.success && res.data) {
        // 将获取到的配置数据存储到config变量中
        config.value = res.data
      } else {
        // 如果API调用失败，设置错误信息
        error.value = res.message || '获取配置失败'
      }
    } catch (err: any) {
      // 如果发生意外错误，设置错误信息
      error.value = err.message || '获取配置失败'
    } finally {
      // 无论成功与否，最后都将loading状态设为false
      loading.value = false
    }
  }

  // 定义一个异步函数来保存配置
  async function saveConfig(newConfig: Partial<Config>): Promise<SaveResult> {
    // 开始加载，将loading状态设为true
    loading.value = true
    // 清除之前的错误信息
    error.value = null

    try {
      // 调用API更新配置
      const res = await updateConfig(newConfig)
      // 如果API调用成功
      if (res.success) {
        // 将新配置合并到现有配置中
        config.value = { ...config.value, ...newConfig }
        // 返回成功结果
        return { success: true, message: '配置已更新' }
      } else {
        // 如果API调用失败，设置错误信息
        error.value = res.message || '更新配置失败'
        // 返回失败结果
        return { success: false, message: error.value || '更新配置失败' }
      }
    } catch (err: any) {
      // 如果发生意外错误，设置错误信息
      error.value = err.message || '更新配置失败'
      // 返回失败结果
      return { success: false, message: error.value || '更新配置失败' }
    } finally {
      // 无论成功与否，最后都将loading状态设为false
      loading.value = false
    }
  }

  // 将store中的变量和函数暴露出去，供其他组件使用
  return {
    config,    // 当前配置数据
    loading,   // 加载状态
    error,     // 错误信息
    fetchConfig,  // 获取配置的函数
    saveConfig    // 保存配置的函数
  }
}) 