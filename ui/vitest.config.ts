/// <reference types="node" />
/// <reference types="vite/client" />
/// <reference types="vitest" />
/// <reference types="vite/client" />
import { defineConfig } from 'vitest/config'
import tsconfigPaths from 'vite-tsconfig-paths'
import * as path from 'path'

// @ts-ignore
import vue from '@vitejs/plugin-vue'

export default defineConfig(() => {
  return {
    plugins: [vue(), tsconfigPaths()],
    resolve: {
      alias: {
        '~~': path.resolve(process.cwd(), '.'),
        '@@': path.resolve(process.cwd(), '.'),
        '~': path.resolve(process.cwd(), '.'),
        '@': path.resolve(process.cwd(), '.'),
        '~~/': path.resolve(process.cwd(), './'),
        '@@/': path.resolve(process.cwd(), './'),
        '~/': path.resolve(process.cwd(), './'),
        '@/': path.resolve(process.cwd(), './'),
        '#app': path.resolve(process.cwd(), './node_modules/nuxt/dist/app')
      }
    },
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
