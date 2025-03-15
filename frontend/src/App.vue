<template>
  <n-config-provider :theme="theme">
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-message-provider>
            <Layout>
              <router-view />
            </Layout>
          </n-message-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { 
  NConfigProvider, 
  NLoadingBarProvider, 
  NDialogProvider, 
  NNotificationProvider, 
  NMessageProvider, 
  darkTheme,
  useOsTheme,
  GlobalTheme
} from 'naive-ui'
import { ref, watchEffect } from 'vue'
import { useThemeStore } from '@/stores/theme'
import Layout from '@/components/Layout.vue'

const themeStore = useThemeStore()
const osTheme = useOsTheme()
const theme = ref<GlobalTheme | null>(null)

watchEffect(() => {
  if (themeStore.isDarkMode === 'auto') {
    theme.value = osTheme.value === 'dark' ? darkTheme : null
  } else {
    theme.value = themeStore.isDarkMode ? darkTheme : null
  }
})
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style> 