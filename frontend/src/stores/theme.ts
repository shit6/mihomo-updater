import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ThemeMode = 'auto' | boolean;

export const useThemeStore = defineStore('theme', () => {
  // 可以是'auto'（跟随系统）, true（暗色主题）或 false（亮色主题）
  const isDarkMode = ref<ThemeMode>(localStorage.getItem('theme-mode') as ThemeMode || 'auto')
  
  function setTheme(mode: ThemeMode): void {
    isDarkMode.value = mode
    localStorage.setItem('theme-mode', String(mode))
  }
  
  return { isDarkMode, setTheme }
}) 