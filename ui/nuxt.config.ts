/// <reference types="node" />
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  nitro: {
    experimental: {
      wasm: true
    }
  },
  experimental: {
    payloadExtraction: false
  },
  runtimeConfig: {
    // Private keys (only available on server-side)
    apiSecret: process.env.API_SECRET,
    
    // Public keys (exposed to client-side)
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000',
      apiTimeout: process.env.API_TIMEOUT || '10000',
      defaultPlaceholderImage: process.env.NUXT_PUBLIC_DEFAULT_PLACEHOLDER_IMAGE || 'https://placehold.co/600x400',
    }
  },
  devServer: {
    host: '0.0.0.0',
    port: 3000
  }
})
