<template>
  <n-layout class="layout">
    <n-layout-header class="header" bordered>
      <div class="header-content">
        <div class="logo">
          <n-icon size="28" :color="isDarkMode ? '#63E2B7' : '#18A058'">
            <FlashOutline />
          </n-icon>
          <span class="logo-text">{{isMobile ? 'Mihomo' : 'Mihomo自动更新服务'}}</span>
        </div>
        <div class="actions">
          <n-space>
            <n-tooltip trigger="hover" placement="bottom">
              <template #trigger>
                <n-button circle @click="handleThemeToggle">
                  <template #icon>
                    <n-icon>
                      <component :is="themeIcon" />
                    </n-icon>
                  </template>
                </n-button>
              </template>
              切换主题
            </n-tooltip>
            <n-tooltip trigger="hover" placement="bottom">
              <template #trigger>
                <n-button circle tag="a" :href="config && 'yacd_url' in config ? config.yacd_url : '#'" target="_blank">
                  <template #icon>
                    <n-icon>
                      <OpenOutline />
                    </n-icon>
                  </template>
                </n-button>
              </template>
              打开Yacd面板
            </n-tooltip>
          </n-space>
        </div>
      </div>
    </n-layout-header>

    <n-layout has-sider position="absolute" style="top: 64px; bottom: 0;">
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="240"
        :collapsed="isMobile"
        :native-scrollbar="false"
        class="sider"
        :show-trigger="isMobile ? false : 'arrow-circle'"
      >
        <n-menu
          :value="activeKey"
          :collapsed="isMobile"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="menuOptions"
          @update:value="handleMenuSelect"
        />
      </n-layout-sider>

      <n-layout-content class="content">
        <div class="content-wrapper">
          <slot />
        </div>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { h, computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NLayout,
  NLayoutHeader,
  NLayoutSider,
  NLayoutContent,
  NMenu,
  NButton,
  NIcon,
  NSpace,
  NTooltip,
  MenuOption
} from 'naive-ui'
import {
  HomeOutline,
  SettingsOutline,
  TimeOutline,
  SunnyOutline,
  MoonOutline,
  ContrastOutline,
  FlashOutline,
  OpenOutline
} from '@vicons/ionicons5'
import { useThemeStore } from '@/stores/theme'
import { useConfigStore } from '@/stores/config'
import { RouterLink } from 'vue-router'

const router = useRouter()
const themeStore = useThemeStore()
const configStore = useConfigStore()
const activeKey = ref(router.currentRoute.value.path)
const isMobile = ref(window.innerWidth <= 768)

// 获取配置
const config = computed(() => configStore.config)

// 监听窗口大小变化
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  if (configStore.config && Object.keys(configStore.config).length === 0) {
    configStore.fetchConfig()
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// 计算主题图标
const themeIcon = computed(() => {
  if (themeStore.isDarkMode === 'auto') {
    return ContrastOutline
  }
  return themeStore.isDarkMode ? MoonOutline : SunnyOutline
})

// 是否为暗色主题
const isDarkMode = computed(() => {
  if (themeStore.isDarkMode === 'auto') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  return themeStore.isDarkMode
})

// 切换主题
const handleThemeToggle = () => {
  const currentTheme = themeStore.isDarkMode
  if (currentTheme === 'auto') {
    themeStore.setTheme(false) // 切换到亮色
  } else if (currentTheme === false) {
    themeStore.setTheme(true) // 切换到暗色
  } else {
    themeStore.setTheme('auto') // 切换到自动
  }
}

// 菜单选择
const handleMenuSelect = (key: string) => {
  router.push(key)
}

// 菜单配置
const menuOptions = computed<MenuOption[]>(() => [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: '/'
        },
        { default: () => '主页' }
      ),
    key: '/',
    icon: () => h(NIcon, null, { default: () => h(HomeOutline) })
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: '/config'
        },
        { default: () => '配置管理' }
      ),
    key: '/config',
    icon: () => h(NIcon, null, { default: () => h(SettingsOutline) })
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: '/history'
        },
        { default: () => '更新历史' }
      ),
    key: '/history',
    icon: () => h(NIcon, null, { default: () => h(TimeOutline) })
  }
])
</script>

<style scoped>
.layout {
  height: 100vh;
}

.header {
  height: 64px;
  padding: 0 24px;
  position: relative;
  z-index: 10;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
}

.sider {
  position: relative;
  z-index: 1;
}

.content {
  padding: 16px;
  overflow: auto;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .logo-text {
    font-size: 16px;
  }

  .header {
    padding: 0 16px;
  }
  
  .content {
    padding: 12px 8px;
  }
  
  .content-wrapper {
    padding: 0 4px;
  }
  
  :deep(.n-data-table-th) {
    font-size: 14px;
  }
  
  :deep(.n-data-table-td) {
    font-size: 14px;
  }
}
</style> 