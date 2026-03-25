<template>
  <header class="bg-white shadow fixed top-0 left-0 right-0 z-40">
    <div class="flex justify-between items-center h-12 px-4">
      <h1 class="text-lg font-bold text-primary-700">ComKit</h1>
      <div class="flex items-center space-x-4">
        <!-- Notification Dropdown -->
        <NotificationDropdown />
        
        <span class="text-sm text-gray-700">{{ $t('header.welcome') }}, {{ user.name }}</span>
        <div class="relative">
          <button @click="showMenu = !showMenu" class="p-2 text-gray-700 hover:bg-gray-100 rounded">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div v-show="showMenu" @click.self="showMenu = false" class="absolute top-full right-0 mt-2 w-56 bg-white border border-gray-200 rounded-md shadow-lg z-20">
            <!-- Language Switcher Section -->
            <div class="border-b border-gray-200 pb-2 mb-2">
              <div class="px-4 py-2">
                <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">{{ $t('common.language') }}</p>
                <div class="flex items-center space-x-2">
                  <button 
                    @click="switchLanguage('en')" 
                    :class="[
                      'px-3 py-1 rounded text-sm font-medium transition-colors',
                      locale === 'en' 
                        ? 'bg-primary-100 text-primary-700' 
                        : 'text-gray-600 hover:bg-gray-100'
                    ]"
                  >
                    🇺🇸 English
                  </button>
                  <button 
                    @click="switchLanguage('id')" 
                    :class="[
                      'px-3 py-1 rounded text-sm font-medium transition-colors',
                      locale === 'id' 
                        ? 'bg-primary-100 text-primary-700' 
                        : 'text-gray-600 hover:bg-gray-100'
                    ]"
                  >
                    🇮🇩 Bahasa
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Navigation Links -->
            <NuxtLink :to="aboutPath" @click="showMenu = false" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              {{ $t('common.about') }}
            </NuxtLink>
            <NuxtLink :to="termsPath" @click="showMenu = false" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              {{ $t('common.terms') }}
            </NuxtLink>
            <button @click="$emit('logout'); showMenu = false" :disabled="isLoggingOut" class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50">
              {{ isLoggingOut ? 'Logging out...' : $t('common.logout') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import NotificationDropdown from './NotificationDropdown.vue'

// Use locale for i18n-aware navigation
const { locale, setLocale } = useI18n()

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

// Generate locale-aware paths
const aboutPath = computed(() => locale.value === 'en' ? '/about' : `/${locale.value}/about`)
const termsPath = computed(() => locale.value === 'en' ? '/terms' : `/${locale.value}/terms`)

// Language switching function
const switchLanguage = (newLocale: string) => {
  setLocale(newLocale)
  showMenu.value = false
}

defineEmits<{
  logout: []
}>()
</script>
