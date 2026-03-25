<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white shadow-lg border-t border-gray-200 z-50">
    <div class="flex justify-around items-center py-2">
      <NuxtLink
        :to="dashboardPath"
        class="flex flex-col items-center justify-center p-2 text-xs font-medium"
        :class="$route.path === dashboardPath ? 'text-primary-300' : 'text-gray-500'"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
        </svg>
        <span>{{ $t('navigation.homepage') }}</span>
      </NuxtLink>
      <NuxtLink
        :to="recipePath"
        class="flex flex-col items-center justify-center p-2 text-xs font-medium"
        :class="$route.path === recipePath ? 'text-primary-300' : 'text-gray-500'"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
        <span>{{ $t('navigation.recipe') }}</span>
      </NuxtLink>
      <NuxtLink
        :to="mypagePath"
        class="flex flex-col items-center justify-center p-2 text-xs font-medium relative"
        :class="$route.path === mypagePath ? 'text-primary-300' : 'text-gray-500'"
      >
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
        </svg>
        <span>{{ $t('navigation.mypage') }}</span>
        <span v-if="displayCount > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">{{ displayCount }}</span>
      </NuxtLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNotifications } from '~~/services/notifications'

// Use localePath for i18n-aware navigation
const { locale } = useI18n()

interface Props {
  incomingRequestsCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  incomingRequestsCount: 0
})

const { unreadCount } = useNotifications()

// Generate locale-aware paths
const dashboardPath = computed(() => locale.value === 'en' ? '/dashboard' : `/${locale.value}/dashboard`)
const recipePath = computed(() => locale.value === 'en' ? '/recipe' : `/${locale.value}/recipe`)
const mypagePath = computed(() => locale.value === 'en' ? '/mypage' : `/${locale.value}/mypage`)

// Check if notifications are enabled
const isNotificationsEnabled = computed(() => {
  // Check runtime config or environment
  if (process.client && typeof window !== 'undefined') {
    // @ts-ignore
    const config = window.__NUXT__?.config?.public
    if (config?.enableNotifications !== undefined) {
      return config.enableNotifications === true
    }
  }
  
  // Check for NUXT_PUBLIC_ENABLE_NOTIFICATIONS environment variable
  if (process.env.NUXT_PUBLIC_ENABLE_NOTIFICATIONS !== undefined) {
    return process.env.NUXT_PUBLIC_ENABLE_NOTIFICATIONS === 'true'
  }
  
  // Fallback to enabled by default
  return true
})

// Use notification unread count, fallback to prop for backward compatibility
const displayCount = computed(() => {
  return isNotificationsEnabled.value ? (unreadCount.value || props.incomingRequestsCount) : 0
})
</script>
