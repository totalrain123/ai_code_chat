import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const repositoryName = process.env.GITHUB_REPOSITORY?.split('/')[1]
const defaultBase = process.env.GITHUB_ACTIONS === 'true' && repositoryName ? `/${repositoryName}/` : '/'

export default defineConfig({
  base: process.env.VITE_BASE_PATH || defaultBase,
  plugins: [vue()],
  server: {
    port: 3000
  }
}) 