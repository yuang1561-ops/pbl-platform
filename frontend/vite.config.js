import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/pbl/',
  server: {
    port: 5173,
    proxy: {
      '/pbl-api': { target: 'http://127.0.0.1:8100', changeOrigin: true }
    }
  }
})
