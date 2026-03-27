import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  root: './src',
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
    proxy: {
      '/chat':   'http://localhost:8000',
      '/health': 'http://localhost:8000',
      '/graph':  'http://localhost:8000',
    },
  },
  build: {
    outDir: '../dist',
    emptyOutDir: true,
  },
})
