<template>
  <div class="history-container">
    <n-card title="更新历史" :bordered="false">
      <template #header-extra>
        <n-space>
          <n-select
            v-model:value="filterValue"
            placeholder="筛选状态"
            :options="filterOptions"
            clearable
            style="width: 100px;"
          />
          <n-button 
            type="primary" 
            @click="refreshHistory" 
            :loading="isLoading"
          >
            <template #icon>
              <n-icon>
                <RefreshOutline />
              </n-icon>
            </template>
            刷新
          </n-button>
        </n-space>
      </template>

      <div v-if="isLoading" class="loading-wrapper">
        <n-spin size="large" />
      </div>
      <div v-else>
        <n-empty v-if="filteredHistory.length === 0" description="暂无更新历史记录" />
        <div v-else>
          <n-space vertical size="medium">
            <div class="history-card-list">
              <div 
                v-for="(item, index) in paginatedHistory" 
                :key="index" 
                class="history-card"
              >
                <n-thing>
                  <template #header>
                    <div class="history-card-header">
                      <n-tag :type="item.success ? 'success' : 'error'" size="small">
                        <template #icon>
                          <n-icon>
                            <component :is="item.success ? CheckmarkOutline : CloseOutline" />
                          </n-icon>
                        </template>
                        {{ item.success ? '成功' : '失败' }}
                      </n-tag>
                      <span class="task-type" :class="item.task.includes('Mihomo') ? 'config-task' : 'geoip-task'">
                        {{ item.task.includes('Mihomo') ? '配置更新' : 'GeoIP更新' }}
                      </span>
                    </div>
                  </template>
                  <template #avatar>
                    <n-icon size="30" :color="item.task.includes('Mihomo') ? '#63E2B7' : '#18A058'">
                      <component :is="item.task.includes('Mihomo') ? DocumentTextOutline : GlobeOutline" />
                    </n-icon>
                  </template>
                  <template #description>
                    <div class="history-card-description">
                      <div class="history-time">
                        <n-icon size="16">
                          <TimeOutline />
                        </n-icon>
                        <span>{{ item.timestamp }}</span>
                      </div>
                      <div v-if="item.message" class="history-message">
                        <n-ellipsis :line-clamp="2" :tooltip="{ width: 250 }">
                          {{ item.message }}
                        </n-ellipsis>
                      </div>
                    </div>
                  </template>
                </n-thing>
              </div>
            </div>
            <div class="pagination-wrapper">
              <n-pagination
                v-model:page="page"
                v-model:page-size="pageSize"
                :item-count="filteredHistory.length"
                :page-sizes="pageSizes"
                show-size-picker
              />
            </div>
          </n-space>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import {
  NCard,
  NButton,
  NIcon,
  NSpin,
  NTag,
  NEmpty,
  NSpace,
  NPagination,
  NThing,
  NSelect,
  NEllipsis
} from 'naive-ui'
import { 
  RefreshOutline, 
  CheckmarkOutline, 
  CloseOutline, 
  TimeOutline, 
  DocumentTextOutline,
  GlobeOutline
} from '@vicons/ionicons5'
import { useHistoryStore } from '@/stores/history'
import { TaskHistory } from '@/types'

const historyStore = useHistoryStore()
const isLoading = ref(true)
const isMobile = ref(window.innerWidth <= 768)
const page = ref(1)
const pageSize = ref(10)
const pageSizes = [5, 10, 20, 30]
const filterValue = ref(null)

const filterOptions = [
  { label: '成功', value: 'success' },
  { label: '失败', value: 'fail' },
  { label: '配置更新', value: 'config' },
  { label: 'GeoIP更新', value: 'geoip' }
]

// 监听窗口大小变化
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  refreshHistory()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// 获取历史记录
const history = computed<TaskHistory[]>(() => historyStore.history || [])

// 过滤后的历史记录
const filteredHistory = computed(() => {
  if (!filterValue.value) return history.value
  
  return history.value.filter(item => {
    if (filterValue.value === 'success') return item.success === true
    if (filterValue.value === 'fail') return item.success === false
    if (filterValue.value === 'config') return item.task.includes('Mihomo')
    if (filterValue.value === 'geoip') return item.task.includes('GeoIP')
    return true
  })
})

// 当前页面显示的历史记录
const paginatedHistory = computed(() => {
  const start = (page.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredHistory.value.slice(start, end)
})

// 监听筛选变化时重置页码
watch(filterValue, () => {
  page.value = 1
})

// 刷新历史记录
const refreshHistory = async () => {
  isLoading.value = true
  try {
    await historyStore.fetchHistory()
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.history-container {
  min-height: 100%;
}

.loading-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.history-card-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.history-card {
  border: 1px solid var(--n-border-color);
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;
}

.history-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.history-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.history-card-description {
  margin-top: 8px;
}

.history-time {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--n-text-color-3);
  font-size: 14px;
  margin-bottom: 4px;
}

.history-message {
  font-size: 14px;
  margin-top: 8px;
}

.task-type {
  font-size: 14px;
}

.config-task {
  color: #63E2B7;
}

.geoip-task {
  color: #18A058;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

@media (max-width: 768px) {
  .history-card-list {
    grid-template-columns: 1fr;
  }
  
  .history-card {
    padding: 12px;
  }
}
</style> 