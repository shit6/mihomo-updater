<template>
  <div class="history-container">
    <n-card title="更新历史" :bordered="false">
      <template #header-extra>
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
          刷新数据
        </n-button>
      </template>

      <div v-if="isLoading" class="loading-wrapper">
        <n-spin size="large" />
      </div>
      <div v-else>
        <n-empty v-if="history.length === 0" description="暂无更新历史记录" />
        <n-data-table
          v-else
          :columns="columns"
          :data="history"
          :pagination="pagination"
          :bordered="false"
          striped
        />
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { h, ref, computed, onMounted } from 'vue'
import {
  NCard,
  NButton,
  NDataTable,
  NIcon,
  NSpin,
  NTag,
  NEmpty,
  DataTableColumns,
  PaginationProps
} from 'naive-ui'
import { RefreshOutline, CheckmarkOutline, CloseOutline } from '@vicons/ionicons5'
import { useHistoryStore } from '@/stores/history'
import { TaskHistory } from '@/types'

const historyStore = useHistoryStore()
const isLoading = ref(true)

// 获取历史记录
const history = computed<TaskHistory[]>(() => historyStore.history || [])

// 表格列配置
const columns: DataTableColumns<TaskHistory> = [
  {
    title: '时间',
    key: 'timestamp',
    width: 180,
    sorter: (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime(),
    defaultSortOrder: 'descend'
  },
  {
    title: '任务类型',
    key: 'task',
    render(row) {
      return row.task === 'Mihomo配置更新' ? 
        h('span', { style: { color: '#63E2B7' } }, '配置更新') : 
        h('span', { style: { color: '#18A058' } }, 'GeoIP更新')
    }
  },
  {
    title: '执行状态',
    key: 'success',
    width: 100,
    render(row) {
      return row.success ? 
        h(
          NTag,
          { type: 'success', size: 'small' },
          {
            default: () => '成功',
            icon: () => h(NIcon, null, { default: () => h(CheckmarkOutline) })
          }
        ) : 
        h(
          NTag,
          { type: 'error', size: 'small' },
          {
            default: () => '失败',
            icon: () => h(NIcon, null, { default: () => h(CloseOutline) })
          }
        )
    },
    filterOptions: [
      { label: '成功', value: 'success' },
      { label: '失败', value: 'fail' }
    ],
    filter(value, row) {
      if (value === 'success') return row.success === true;
      if (value === 'fail') return row.success === false;
      return true;
    }
  },
  {
    title: '详细信息',
    key: 'message',
    ellipsis: {
      tooltip: true
    }
  }
]

// 分页配置
const pagination = ref<PaginationProps>({
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 30, 50],
  onChange: (page) => {
    pagination.value.page = page
  },
  onUpdatePageSize: (pageSize) => {
    pagination.value.pageSize = pageSize
    pagination.value.page = 1
  }
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

onMounted(async () => {
  await refreshHistory()
})
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
</style> 