<template>
  <header class="bg-white shadow fixed top-0 left-0 right-0 z-40">
    <div class="flex justify-between items-center h-12 px-4">
      <h1 class="text-lg font-bold text-primary-700">ComKit</h1>
      <div class="flex items-center space-x-4">
        <!-- Notification Dropdown -->
        <NotificationDropdown />
        
        <span class="text-sm text-gray-700">Welcome, {{ user.name }}</span>
        <div class="relative">
          <button @click="showMenu = !showMenu" class="p-2 text-gray-700 hover:bg-gray-100 rounded">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div v-show="showMenu" @click.self="showMenu = false" class="absolute top-full right-0 mt-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-20">
            <NuxtLink to="/about" @click="showMenu = false" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              Tentang Kami
            </NuxtLink>
            <NuxtLink to="/terms" @click="showMenu = false" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              Terms & Conditions
            </NuxtLink>
            <button @click="$emit('logout'); showMenu = false" :disabled="isLoggingOut" class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50">
              {{ isLoggingOut ? 'Logging out...' : 'Logout' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NotificationDropdown from './NotificationDropdown.vue'

interface Props {
  user: {
    name: string
    username: string
  }
  isLoggingOut?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isLoggingOut: false
})

const showMenu = ref(false)

defineEmits<{
  logout: []
}>()
</script>
