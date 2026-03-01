/// <reference types="node" />
/// <reference types="vite/client" />
/// <reference types="vitest" />
/// <reference types="vite/client" />
import { defineConfig } from 'vitest/config'
import tsconfigPaths from 'vite-tsconfig-paths'
// @ts-ignore
import vue from '@vitejs/plugin-vue'

export default defineConfig(async () => {
  
  return {
    plugins: [vue(), tsconfigPaths()],
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: ['./test/setup.ts']
    },
    optimizeDeps: {
      disabled: true
    }
  }
})
