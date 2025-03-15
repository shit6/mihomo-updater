import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'] // 确保vite能正确解析不同的扩展名
  },
  server: {
    port: 3000,
    host: true, // 监听所有地址，便于远程访问
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    },
    fs: {
      // 允许访问上层目录，用于源码映射
      strict: false
    },
    // 启用源码映射
    sourcemapIgnoreList: false,
  },
  // 始终启用源码映射，便于调试
  build: {
    sourcemap: true,
  }
}) 