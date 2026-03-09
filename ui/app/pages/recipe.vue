<template>
  <div class="min-h-screen bg-gray-50 mobile-container">
    <TopHeader :user="user" :is-logging-out="isLoggingOut" @logout="handleLogout" />

    <!-- Main Content -->
    <main class="pt-12 pb-16 px-4">
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">AI Recipe Generator</h2>

        <!-- Input Section -->
        <div class="mb-6">
          <label for="ingredients" class="block text-sm font-medium text-gray-700 mb-2">
            Ingredients you have:
          </label>
          <textarea
            id="ingredients"
            v-model="ingredients"
            data-testid="ingredients-textarea"
            rows="4"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            placeholder="Enter ingredients you have, separated by commas. Example: tomato, onion, garlic, pasta, olive oil"
            :disabled="isLoading"
          ></textarea>
          <p class="mt-1 text-sm text-gray-500">
            Enter the ingredients you have available and AI will generate a recipe for you.
          </p>
        </div>

        <!-- Generate Button -->
        <div class="mb-6">
          <button
            @click="generateRecipe"
            data-testid="generate-btn"
            :disabled="!ingredients.trim() || isLoading"
            class="w-full sm:w-auto px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" data-testid="loading-spinner" class="mr-2">
              <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isLoading ? 'Generating Recipe...' : 'Generate Recipe' }}
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="error" data-testid="error-message" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Error</h3>
              <div class="mt-2 text-sm text-red-700">
                {{ error }}
              </div>
            </div>
          </div>
        </div>

        <!-- Recipe Output -->
        <div v-if="recipe" data-testid="recipe-container" class="border-t pt-6">
          <h3 data-testid="recipe-title" class="text-xl font-semibold text-gray-900 mb-4">{{ recipe.title }}</h3>

          <!-- Recipe Meta Info -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            <div class="bg-gray-50 p-3 rounded-lg">
              <div class="text-sm text-gray-500">Cooking Time</div>
              <div data-testid="recipe-cooking-time" class="font-medium text-gray-900">{{ recipe.cooking_time }} minutes</div>
            </div>
            <div class="bg-gray-50 p-3 rounded-lg">
              <div class="text-sm text-gray-500">Servings</div>
              <div data-testid="recipe-servings" class="font-medium text-gray-900">{{ recipe.servings }} servings</div>
            </div>
            <div class="bg-gray-50 p-3 rounded-lg">
              <div class="text-sm text-gray-500">Difficulty</div>
              <div data-testid="recipe-difficulty" class="font-medium text-gray-900 capitalize">{{ recipe.difficulty }}</div>
            </div>
          </div>

          <!-- Ingredients -->
          <div class="mb-6">
            <h4 class="text-lg font-medium text-gray-900 mb-3">Ingredients:</h4>
            <ul class="list-disc list-inside space-y-1">
              <li v-for="ingredient in recipe.ingredients" :key="ingredient" data-testid="recipe-ingredient" class="text-gray-700">
                {{ ingredient }}
              </li>
            </ul>
          </div>

          <!-- Instructions -->
          <div class="mb-6">
            <h4 class="text-lg font-medium text-gray-900 mb-3">Instructions:</h4>
            <ol class="list-decimal list-inside space-y-2">
              <li v-for="(instruction, index) in recipe.instructions" :key="index" data-testid="recipe-instruction" class="text-gray-700">
                {{ instruction }}
              </li>
            </ol>
          </div>

          <!-- Raw Text (fallback) -->
          <div v-if="recipe.raw_text" class="mb-6">
            <h4 class="text-lg font-medium text-gray-900 mb-3">Additional Information:</h4>
            <div class="bg-gray-50 p-4 rounded-lg">
              <pre class="whitespace-pre-wrap text-gray-700">{{ recipe.raw_text }}</pre>
            </div>
          </div>

          <!-- Generated At -->
          <div data-testid="generated-at" class="text-sm text-gray-500 text-right">
            Generated at: {{ generatedAt ? new Date(generatedAt).toLocaleString() : '' }}
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-8">
          <div class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-primary-700 bg-primary-100">
            <svg class="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            AI is generating your recipe...
          </div>
        </div>
      </div>
    </main>

    <!-- Bottom Navigation -->
    <BottomNavigation />

    <AuthLoadingOverlay :is-authenticating="isAuthenticating" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuth } from "~~/composables/useAuth"
import { aiApi, type RecipeResponse } from "~~/services/api"
import AuthLoadingOverlay from "~~/components/AuthLoadingOverlay.vue"
import BottomNavigation from '~~/components/BottomNavigation.vue'
import TopHeader from '~~/components/TopHeader.vue'

// Page metadata
definePageMeta({
  title: 'Recipe - ComKit',
  description: 'AI Recipe Generator'
})

// Use auth composable
const { user: authUser, logout } = useAuth()

// Computed user data from auth
const user = computed(() => authUser.value || { name: 'User', username: 'user' })

// Authentication check
onMounted(async () => {
  // Check authentication on client side
  if (process.client) {
    isAuthenticating.value = true
    try {
      const { authApi } = await import('~~/services/api')
      await authApi.validateCookies()
      // If successful, allow the page to work normally
    } catch (error) {
      // Redirect to login if not authenticated
      await navigateTo('/login')
    } finally {
      isAuthenticating.value = false
    }
  }
})

// State
const ingredients = ref('')
const recipe = ref<RecipeResponse['recipe'] | null>(null)
const generatedAt = ref<string>('')
const isLoading = ref(false)
const error = ref('')
const isLoggingOut = ref(false)
const isAuthenticating = ref(false)

// Methods
const generateRecipe = async () => {
  if (!ingredients.value.trim()) {
    error.value = 'Please enter some ingredients'
    return
  }

  isLoading.value = true
  error.value = ''
  recipe.value = null

  try {
    const response = await aiApi.generateRecipe({
      ingredients: ingredients.value.trim()
    })
    
    recipe.value = response.recipe
    generatedAt.value = response.generated_at
  } catch (err: any) {
    console.error('Error generating recipe:', err)
    error.value = err.detail || 'Failed to generate recipe. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleLogout = async () => {
  isLoggingOut.value = true
  try {
    await logout()
    await navigateTo('/login')
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    isLoggingOut.value = false
  }
}
</script>

<style scoped>
.mobile-container {
  max-width: 375px;
  margin: 0 auto;
}
</style>
