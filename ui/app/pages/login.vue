<template>
  <div class="min-h-screen mobile-container">
    <div class="min-h-screen flex flex-col justify-center p-8 bg-white">
      <div class="w-full max-w-sm mx-auto space-y-8">
        <div>
          <h2 class="text-3xl font-extrabold text-gray-900">Welcome back</h2>
          <p class="mt-2 text-sm text-gray-600">
            Don't have an account?
            <NuxtLink to="/register" class="font-medium text-primary-100 hover:text-primary-200">
              Sign up now
            </NuxtLink>
          </p>
          <p class="mt-1 text-sm text-gray-600">
            <NuxtLink to="/about" class="font-medium text-primary-100 hover:text-primary-200">
              About ComKit
            </NuxtLink>
          </p>
        </div>

        <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
          <div class="space-y-4">
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
              <input 
                id="username" 
                v-model="form.username" 
                type="text" 
                required 
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-400 focus:border-primary-400" 
                placeholder="Enter username" 
                :disabled="loading"
              />
            </div>
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input 
                id="password" 
                v-model="form.password" 
                type="password" 
                required 
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-400 focus:border-primary-400" 
                placeholder="••••••••" 
                :disabled="loading"
              />
            </div>
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center text-sm text-gray-900">
              <input 
                v-model="form.rememberMe" 
                type="checkbox" 
                class="h-4 w-4 text-primary-400 border-gray-300 rounded" 
                :disabled="loading"
              />
              <span class="ml-2">Remember me</span>
            </label>
            <a href="#" class="text-sm font-medium text-primary-100 hover:text-primary-200">Forgot?</a>
          </div>

          <button 
            type="submit" 
            :disabled="loading" 
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-400 hover:bg-primary-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'Signing in...' : 'Sign in to account' }}
          </button>
        </form>

        <!-- Error Message -->
        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">
                {{ error }}
              </h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '~~/composables/useAuth'

import guestMiddleware from "~~/middleware/guest.client"

// Page metadata
definePageMeta({
  title: 'Login - ComKit',
  description: 'Sign in to your ComKit account',
  middleware: guestMiddleware
})

// Use auth composable
const { login, isLoading, error } = useAuth()

// Local loading state for form inputs
const loading = isLoading

// Form data interface
interface LoginForm {
  username: string
  password: string
  rememberMe: boolean
}

// Form data
const form = ref<LoginForm>({
  username: '',
  password: '',
  rememberMe: false
})

// Methods
const handleLogin = async (): Promise<void> => {
  if (!form.value.username || !form.value.password) {
    return
  }

  try {
    await login(form.value.username, form.value.password, form.value.rememberMe)
    
    // Redirect to dashboard on successful login
    await navigateTo('/dashboard')
  } catch (err) {
    // Error is already handled by the auth composable
    console.error('Login failed:', err)
  }
}
</script>

<style scoped>
/* Additional styles if needed */
.mobile-container {
  max-width: 375px;
  margin: 0 auto;
}
</style>
