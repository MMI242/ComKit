<template>
  <div class="min-h-screen flex flex-col md:flex-row font-sans">
    <div class="hidden md:flex md:w-1/2 bg-indigo-600 p-12 flex-col justify-between text-white">
      <div>
        <h1 class="text-4xl font-bold tracking-tight">ComKit</h1>
        <p class="mt-4 text-indigo-100 text-lg">Platform berbagi komunitas untuk mempermudah hidup Anda.</p>
      </div>
      <div>
        <p class="text-sm text-indigo-200">&copy; 2026 ComKit Inc.</p>
      </div>
    </div>

    <div class="w-full md:w-1/2 flex items-center justify-center p-8 bg-white">
      <div class="w-full max-w-sm space-y-8">
        <div>
          <h2 class="text-3xl font-extrabold text-gray-900">Welcome back</h2>
          <p class="mt-2 text-sm text-gray-600">
            Don't have an account?
            <NuxtLink to="/register" class="font-medium text-indigo-600 hover:text-indigo-500">
              Sign up now
            </NuxtLink>
          </p>
        </div>

        <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
          <div class="space-y-4">
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
              <input id="username" v-model="form.username" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" placeholder="Enter username" />
            </div>
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input id="password" v-model="form.password" type="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" placeholder="••••••••" />
            </div>
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center text-sm text-gray-900">
              <input v-model="form.rememberMe" type="checkbox" class="h-4 w-4 text-indigo-600 border-gray-300 rounded" />
              <span class="ml-2">Remember me</span>
            </label>
            <a href="#" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">Forgot?</a>
          </div>

          <button type="submit" :disabled="loading" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all">
            {{ loading ? 'Signing in...' : 'Sign in to account' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Page metadata
definePageMeta({
  title: 'Login - ComKit',
  description: 'Sign in to your ComKit account'
})

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

// State
const loading = ref<boolean>(false)
const error = ref<string>('')

// Methods
const handleLogin = async (): Promise<void> => {
  loading.value = true
  error.value = ''

  try {
    // TODO: Implement actual login logic
    // For now, simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock validation
    if (form.value.username === 'test' && form.value.password === 'password') {
      // TODO: Store auth token and redirect
      await navigateTo('/dashboard')
    } else {
      error.value = 'Invalid username or password'
    }
  } catch (err: any) {
    error.value = 'An error occurred during login. Please try again.'
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Additional styles if needed */
</style>
