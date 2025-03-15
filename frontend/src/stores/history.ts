import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTaskHistory } from '@/api/history'
import { TaskHistory } from '@/types'

export const useHistoryStore = defineStore('history', () => {
    const history = ref<TaskHistory[]>([])
    const loading = ref<boolean>(false)
    const error = ref<string | null>(null)

    async function fetchHistory(): Promise<void> {
        loading.value = true
        error.value = null

        try {
            const res = await getTaskHistory()
            if (res.success && res.data) {
                history.value = res.data
            } else {
                error.value = res.message || '获取历史记录失败'
            }
        } catch (err: any) {
            error.value = err.message || '获取历史记录失败'
        } finally {
            loading.value = false
        }
    }

    return {
        history,
        loading,
        error,
        fetchHistory
    }
}) 