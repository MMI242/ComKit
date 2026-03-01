/// <reference types="node" />
/// <reference types="nuxt" />
// Auth plugin to initialize auth state on app startup
import { useAuth } from "../composables/useAuth"
import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  // Initialize auth state when app starts
  if (process.client) {
    const { initAuth } = useAuth()
    initAuth()
  }
})
