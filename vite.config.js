import { defineConfig } from 'vite'

export default defineConfig(({ mode }) => ({
  root: 'frontend',
  base: mode === 'demo' ? '/data-agent/' : '/',
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/health': 'http://127.0.0.1:8000',
    },
  },
  build: {
    outDir: mode === 'demo' ? 'demo-dist' : 'dist',
    emptyOutDir: true,
  },
}))
