import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // ← このブロックを追加
    },
  },
  server: {
    proxy: {
      '/api': 'http://localhost:5000', // APIサーバーのポートに合わせて変更(ローカル開発用)
    }
  }
})
