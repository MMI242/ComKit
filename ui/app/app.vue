<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useNotifications } from '~~/services/notifications'

// Initialize notification service
const { connect, disconnect } = useNotifications()

onMounted(() => {
  // Connect to WebSocket when app mounts
  if (process.client) {
    // Check if notifications are enabled
    let notificationsEnabled = true
    
    if (typeof window !== 'undefined') {
      // @ts-ignore
      const config = window.__NUXT__?.config?.public
      if (config?.enableNotifications !== undefined) {
        notificationsEnabled = config.enableNotifications === true
      }
    }
    
    // Check for NUXT_PUBLIC_ENABLE_NOTIFICATIONS environment variable
    if (process.env.NUXT_PUBLIC_ENABLE_NOTIFICATIONS !== undefined) {
      notificationsEnabled = process.env.NUXT_PUBLIC_ENABLE_NOTIFICATIONS === 'true'
    }
    
    if (notificationsEnabled) {
      connect()
    }
  }
})

onUnmounted(() => {
  // Disconnect WebSocket when app unmounts
  if (process.client) {
    disconnect()
  }
})
</script>

<style>
/* Import custom color styles */
@import '../assets/styles/colors.css';

/* Global styles */
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}
</style>
