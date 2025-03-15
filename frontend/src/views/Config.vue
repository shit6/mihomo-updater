<template>
  <div class="config-container">
    <n-card title="配置管理" :bordered="false">
      <template #header-extra>
        <n-space>
          <n-button @click="resetForm" :disabled="isLoading">
            <template #icon>
              <n-icon>
                <RefreshOutline />
              </n-icon>
            </template>
            重置表单
          </n-button>
          <n-button type="primary" @click="saveConfig" :loading="isSaving">
            <template #icon>
              <n-icon>
                <SaveOutline />
              </n-icon>
            </template>
            保存配置
          </n-button>
        </n-space>
      </template>

      <div v-if="isLoading" class="loading-wrapper">
        <n-spin size="large" />
      </div>
      <div v-else>
        <n-form
          ref="formRef"
          :model="formData"
          :rules="rules"
          label-placement="left"
          label-width="auto"
          require-mark-placement="right-hanging"
          :style="{ maxWidth: '850px' }"
        >
          <n-h3 prefix="bar">基本配置</n-h3>
          <n-grid :cols="gridCols" :x-gap="24">
            <n-grid-item>
              <n-form-item label="配置拉取地址" path="fetch_url">
                <n-input
                  v-model:value="formData.fetch_url"
                  placeholder="请输入配置拉取地址"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="拉取间隔（秒）" path="fetch_interval">
                <n-input-number
                  v-model:value="formData.fetch_interval"
                  :min="60"
                  :max="86400"
                  placeholder="请输入拉取间隔"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-grid :cols="gridCols" :x-gap="24">
            <n-grid-item>
              <n-form-item label="GeoIP更新间隔（秒）" path="geoip_fetch_interval">
                <n-input-number
                  v-model:value="formData.geoip_fetch_interval"
                  :min="3600"
                  :max="604800"
                  placeholder="请输入GeoIP更新间隔"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="Web服务端口" path="web_port">
                <n-input-number
                  v-model:value="formData.web_port"
                  :min="1"
                  :max="65535"
                  placeholder="请输入Web服务端口"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-h3 prefix="bar">文件路径配置</n-h3>
          <n-grid :cols="gridCols" :x-gap="24">
            <n-grid-item>
              <n-form-item label="Mihomo配置文件路径" path="mihomo_config_path">
                <n-input
                  v-model:value="formData.mihomo_config_path"
                  placeholder="请输入Mihomo配置文件路径"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="备份目录" path="backup_dir">
                <n-input
                  v-model:value="formData.backup_dir"
                  placeholder="请输入备份目录"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-h3 prefix="bar">GeoIP数据配置</n-h3>
          <n-grid :cols="gridCols" :x-gap="24">
            <n-grid-item>
              <n-form-item label="GeoIP数据文件路径" path="geoip_path">
                <n-input
                  v-model:value="formData.geoip_path"
                  placeholder="请输入GeoIP数据文件路径"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="GeoSite数据文件路径" path="geosite_path">
                <n-input
                  v-model:value="formData.geosite_path"
                  placeholder="请输入GeoSite数据文件路径"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-grid :cols="gridCols" :x-gap="24">
            <n-grid-item>
              <n-form-item label="MMDB数据文件路径" path="mmdb_path">
                <n-input
                  v-model:value="formData.mmdb_path"
                  placeholder="请输入MMDB数据文件路径"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
            </n-grid-item>
          </n-grid>

          <n-h3 prefix="bar">下载地址配置</n-h3>
          <n-grid :cols="gridCols" :x-gap="24">
            <n-grid-item>
              <n-form-item label="GeoIP下载地址" path="geoip_url">
                <n-input
                  v-model:value="formData.geoip_url"
                  placeholder="请输入GeoIP下载地址"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="GeoSite下载地址" path="geosite_url">
                <n-input
                  v-model:value="formData.geosite_url"
                  placeholder="请输入GeoSite下载地址"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-grid :cols="gridCols" :x-gap="24">
            <n-grid-item>
              <n-form-item label="MMDB下载地址" path="mmdb_url">
                <n-input
                  v-model:value="formData.mmdb_url"
                  placeholder="请输入MMDB下载地址"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
            </n-grid-item>
          </n-grid>
          
          <n-h3 prefix="bar">Yacd面板配置</n-h3>
          <n-grid :cols="gridCols" :x-gap="24">
            <n-grid-item>
              <n-form-item label="Yacd面板地址" path="yacd_url">
                <n-input
                  v-model:value="formData.yacd_url"
                  placeholder="请输入Yacd面板地址"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="Clash API地址" path="clash_api_url">
                <n-input
                  v-model:value="formData.clash_api_url"
                  placeholder="请输入Clash API地址"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </n-form>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, reactive, onMounted } from 'vue'
import {
  NCard,
  NButton,
  NSpace,
  NH3,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NGrid,
  NGridItem,
  NIcon,
  NSpin,
  useMessage,
  FormRules,
  FormInst
} from 'naive-ui'
import { RefreshOutline, SaveOutline } from '@vicons/ionicons5'
import { useConfigStore } from '@/stores/config'
import { Config } from '@/types'

const message = useMessage()
const configStore = useConfigStore()
const formRef = ref<FormInst | null>(null)
const isLoading = ref(true)
const isSaving = ref(false)

// 默认配置
const defaultForm: Config = {
  fetch_url: '',
  fetch_interval: 3600,
  geoip_fetch_interval: 86400,
  mihomo_config_path: '/etc/mihomo/config.yaml',
  backup_dir: '/etc/mihomo/backups',
  geoip_url: '',
  geosite_url: '',
  mmdb_url: '',
  geoip_path: '/etc/mihomo/geoip.dat',
  geosite_path: '/etc/mihomo/geosite.dat',
  mmdb_path: '/etc/mihomo/country.mmdb',
  yacd_url: '',
  clash_api_url: '',
  web_port: 5000
}

// 表单数据
const formData = reactive<Config>({ ...defaultForm })

// 根据屏幕宽度调整网格列数
const gridCols = computed(() => {
  return window.innerWidth <= 768 ? 1 : 2
})

// 表单验证规则
const rules: FormRules = {
  fetch_url: {
    required: true,
    message: '请输入配置拉取地址',
    trigger: 'blur'
  },
  fetch_interval: {
    required: true,
    type: 'number',
    message: '请输入有效的拉取间隔',
    trigger: ['blur', 'change']
  },
  geoip_fetch_interval: {
    required: true,
    type: 'number',
    message: '请输入有效的GeoIP更新间隔',
    trigger: ['blur', 'change']
  },
  mihomo_config_path: {
    required: true,
    message: '请输入Mihomo配置文件路径',
    trigger: 'blur'
  },
  backup_dir: {
    required: true,
    message: '请输入备份目录',
    trigger: 'blur'
  },
  geoip_path: {
    required: true,
    message: '请输入GeoIP数据文件路径',
    trigger: 'blur'
  },
  geosite_path: {
    required: true,
    message: '请输入GeoSite数据文件路径',
    trigger: 'blur'
  },
  mmdb_path: {
    required: true,
    message: '请输入MMDB数据文件路径',
    trigger: 'blur'
  },
  web_port: {
    required: true,
    type: 'number',
    message: '请输入有效的Web服务端口',
    trigger: ['blur', 'change']
  }
}

// 载入配置
const loadConfig = async () => {
  isLoading.value = true
  try {
    await configStore.fetchConfig()
    const config = configStore.config as Config
    
    // 将配置数据赋值给表单
    Object.keys(formData).forEach(key => {
      if (config[key] !== undefined) {
        formData[key] = config[key]
      }
    })
  } catch (error) {
    message.error('获取配置失败')
  } finally {
    isLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  loadConfig()
}

// 保存配置
const saveConfig = async () => {
  if (!formRef.value) return
  
  formRef.value.validate(async (errors) => {
    if (errors) {
      message.error('表单验证失败，请检查填写内容')
      return
    }
    
    isSaving.value = true
    try {
      const result = await configStore.saveConfig(formData)
      if (result.success) {
        message.success(result.message)
      } else {
        message.error(result.message)
      }
    } catch (error) {
      message.error('保存配置失败')
    } finally {
      isSaving.value = false
    }
  })
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.config-container {
  min-height: 100%;
}

.loading-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}
</style> 