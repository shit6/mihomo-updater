<template>
  <div class="home-container">
    <n-card title="Mihomo自动更新服务" class="welcome-card">
      <template #header-extra>
        <n-space>
          <n-button type="primary" @click="refreshData" :loading="isLoading">
            <template #icon>
              <n-icon>
                <RefreshOutline />
              </n-icon>
            </template>
            刷新状态
          </n-button>
        </n-space>
      </template>

      <div v-if="isLoading" class="loading-wrapper">
        <n-spin size="large" />
      </div>
      <div v-else>
        <n-grid :cols="gridCols" :x-gap="16" :y-gap="16">
          <!-- 状态概述 -->
          <n-grid-item>
            <n-card title="系统状态" size="small">
              <n-descriptions bordered label-placement="left" :column="1">
                <n-descriptions-item label="服务状态">
                  <n-tag type="success">
                    <template #icon>
                      <n-icon>
                        <CheckmarkOutline />
                      </n-icon>
                    </template>
                    运行中
                  </n-tag>
                </n-descriptions-item>
                <n-descriptions-item label="最近更新">
                  <span v-if="lastUpdate">{{ lastUpdate }}</span>
                  <n-text v-else depth="3">暂无记录</n-text>
                </n-descriptions-item>
                <n-descriptions-item label="更新结果">
                  <n-tag v-if="lastResult?.success" type="success">
                    <template #icon>
                      <n-icon>
                        <CheckmarkOutline />
                      </n-icon>
                    </template>
                    成功
                  </n-tag>
                  <n-tag v-else-if="lastResult" type="error">
                    <template #icon>
                      <n-icon>
                        <CloseOutline />
                      </n-icon>
                    </template>
                    失败
                  </n-tag>
                  <n-text v-else depth="3">暂无记录</n-text>
                </n-descriptions-item>
              </n-descriptions>
            </n-card>
          </n-grid-item>

          <!-- 更新操作 -->
          <n-grid-item>
            <n-card title="更新操作" size="small">
              <n-space vertical>
                <n-button
                  type="primary"
                  block
                  @click="updateMihomoConfig"
                  :loading="updatingMihomo"
                >
                  <template #icon>
                    <n-icon>
                      <CloudDownloadOutline />
                    </n-icon>
                  </template>
                  更新Mihomo配置
                </n-button>
                <n-button
                  type="info"
                  block
                  @click="updateGeoData"
                  :loading="updatingGeo"
                >
                  <template #icon>
                    <n-icon>
                      <GlobeOutline />
                    </n-icon>
                  </template>
                  更新GeoIP数据
                </n-button>
                <n-button
                  type="warning"
                  block
                  @click="selectLocalFile"
                  :loading="importingYaml"
                >
                  <template #icon>
                    <n-icon>
                      <FolderOpenOutline />
                    </n-icon>
                  </template>
                  从本地文件导入
                </n-button>
                <input 
                  ref="fileInputRef" 
                  type="file" 
                  accept=".yaml,.yml" 
                  style="display: none;" 
                  @change="handleFileSelected" 
                />
              </n-space>
            </n-card>
          </n-grid-item>

          <!-- 配置信息 -->
          <n-grid-item :span="gridCols">
            <n-card title="配置信息" size="small">
              <n-descriptions bordered label-placement="left" :column="detailsCols">
                <n-descriptions-item label="Mihomo配置文件">
                  {{ config.mihomo_config_path || '-' }}
                </n-descriptions-item>
                <n-descriptions-item label="备份目录">
                  {{ config.backup_dir || '-' }}
                </n-descriptions-item>
                <n-descriptions-item label="配置拉取间隔">
                  {{ formatInterval(config.fetch_interval) || '-' }}
                </n-descriptions-item>
                <n-descriptions-item label="GeoIP更新间隔">
                  {{ formatInterval(config.geoip_fetch_interval) || '-' }}
                </n-descriptions-item>
                <n-descriptions-item label="Yacd地址">
                  <n-button text tag="a" :href="config.yacd_url" target="_blank">
                    {{ config.yacd_url || '-' }}
                  </n-button>
                </n-descriptions-item>
                <n-descriptions-item label="API地址">
                  <n-button text tag="a" :href="config.clash_api_url" target="_blank">
                    {{ config.clash_api_url || '-' }}
                  </n-button>
                </n-descriptions-item>
              </n-descriptions>
            </n-card>
          </n-grid-item>
        </n-grid>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import {
  NCard,
  NButton,
  NSpace,
  NGrid,
  NGridItem,
  NDescriptions,
  NDescriptionsItem,
  NTag,
  NIcon,
  NSpin,
  NText,
  useMessage
} from 'naive-ui'
import {
  RefreshOutline,
  CheckmarkOutline,
  CloseOutline,
  CloudDownloadOutline,
  GlobeOutline,
  FolderOpenOutline
} from '@vicons/ionicons5'
import { useConfigStore } from '@/stores/config'
import { useHistoryStore } from '@/stores/history'
import { updateMihomo, updateGeoIP, importLocalYaml } from '@/api/updater'
import { Config, TaskHistory } from '@/types'

const configStore = useConfigStore()
const historyStore = useHistoryStore()
const message = useMessage()

const isLoading = ref(true)
const updatingMihomo = ref(false)
const updatingGeo = ref(false)
const importingYaml = ref(false)
const fileInputRef = ref<HTMLInputElement | null>(null)

// 根据屏幕宽度调整网格列数
const gridCols = computed(() => {
  return window.innerWidth <= 768 ? 1 : 2
})

// 根据屏幕宽度调整描述列数
const detailsCols = computed(() => {
  return window.innerWidth <= 768 ? 1 : 2
})

// 获取配置
const config = computed<Config>(() => configStore.config as Config)

// 最后更新记录
const lastResult = computed<TaskHistory | null>(() => {
  if (historyStore.history && historyStore.history.length > 0) {
    return historyStore.history[0]
  }
  return null
})

// 最后更新时间
const lastUpdate = computed(() => {
  if (lastResult.value) {
    return lastResult.value.timestamp
  }
  return null
})

// 格式化时间间隔
const formatInterval = (seconds: number): string => {
  if (!seconds) return '未设置'
  
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  
  if (hours > 0) {
    return `${hours}小时${minutes > 0 ? ` ${minutes}分钟` : ''}`
  } else if (minutes > 0) {
    return `${minutes}分钟`
  } else {
    return `${seconds}秒`
  }
}

// 刷新数据
const refreshData = async () => {
  isLoading.value = true
  try {
    await Promise.all([
      configStore.fetchConfig(),
      historyStore.fetchHistory()
    ])
  } finally {
    isLoading.value = false
  }
}

// 更新Mihomo配置
const updateMihomoConfig = async () => {
  updatingMihomo.value = true
  try {
    await updateMihomo()
    await historyStore.fetchHistory()
    message.success('Mihomo配置更新成功')
  } catch (error) {
    message.error(`更新失败: ${(error as Error).message}`)
  } finally {
    updatingMihomo.value = false
  }
}

// 更新GeoIP数据
const updateGeoData = async () => {
  updatingGeo.value = true
  try {
    await updateGeoIP()
    await historyStore.fetchHistory()
    message.success('GeoIP数据更新成功')
  } catch (error) {
    message.error(`更新失败: ${(error as Error).message}`)
  } finally {
    updatingGeo.value = false
  }
}

// 选择本地文件
const selectLocalFile = () => {
  fileInputRef.value?.click()
}

// 处理选择的文件
const handleFileSelected = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || input.files.length === 0) {
    return
  }
  
  const file = input.files[0]
  importingYaml.value = true
  
  try {
    await importLocalYaml(file)
    await historyStore.fetchHistory()
    message.success('从本地文件导入配置成功')
  } catch (error) {
    message.error(`导入失败: ${(error as Error).message}`)
  } finally {
    importingYaml.value = false
    // 重置文件输入框
    if (fileInputRef.value) {
      fileInputRef.value.value = ''
    }
  }
}

onMounted(async () => {
  await refreshData()
})
</script>

<style scoped>
.home-container {
  height: 100%;
}

.welcome-card {
  margin-bottom: 16px;
}

.loading-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}
</style> 