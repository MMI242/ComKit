<template>
  <div class="w-full inline-flex items-center p-1 bg-gray-100 rounded-lg">
    <button 
      @click="switchLanguage('en')" 
      :class="[
        'flex-1 px-3 py-1.5 rounded-md text-sm font-medium transition-all duration-200',
        locale === 'en' 
          ? 'bg-white text-primary-700 shadow-sm' 
          : 'text-gray-600 hover:text-gray-900'
      ]"
    >
      🇺🇸 English
    </button>
    <button 
      @click="switchLanguage('id')" 
      :class="[
        'flex-1 px-3 py-1.5 rounded-md text-sm font-medium transition-all duration-200',
        locale === 'id' 
          ? 'bg-white text-primary-700 shadow-sm' 
          : 'text-gray-600 hover:text-gray-900'
      ]"
    >
      🇮🇩 Bahasa
    </button>
  </div>
</template>

<script setup lang="ts">
const { locale, setLocale } = useI18n()

const switchLanguage = (newLocale: 'en' | 'id') => {
  setLocale(newLocale)
}
</script>
