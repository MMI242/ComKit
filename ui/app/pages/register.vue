<template>
  <div class="min-h-screen mobile-container">
    <div class="min-h-screen flex flex-col justify-center p-8 relative overflow-hidden">
      <!-- Background -->
      <div class="absolute inset-0 bg-gray-50"></div>

      <!-- Form container -->
      <div class="relative w-full max-w-md mx-auto">
        <!-- Logo/Brand -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-primary-300 via-primary-400 to-primary-500 rounded-2xl mb-4 shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
            </svg>
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-primary-400 to-primary-500 bg-clip-text text-transparent">
            Join ComKit
          </h1>
          <p class="mt-2 text-gray-600">Start sharing kitchen items with your community</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleRegister" class="space-y-5">
          <!-- Name -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
              Full Name
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <input
                id="name"
                v-model="form.name"
                name="name"
                type="text"
                required
                class="pl-10 w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm"
                placeholder="John Doe"
              />
            </div>
          </div>

          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
                </svg>
              </div>
              <input
                id="username"
                v-model="form.username"
                name="username"
                type="text"
                required
                class="pl-10 w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm"
                placeholder="@johndoe"
              />
            </div>
          </div>

          <!-- Address -->
          <div>
            <label for="address" class="block text-sm font-medium text-gray-700 mb-1">
              Address
            </label>
            <div class="relative">
              <div class="absolute top-3 left-0 pl-3 flex items-start pointer-events-none">
                <svg class="h-5 w-5 text-gray-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
              </div>
              <textarea
                id="address"
                v-model="form.address"
                name="address"
                rows="2"
                required
                class="pl-10 w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm resize-none"
                placeholder="123 Main St, City, State 12345"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                required
                class="pl-10 w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm"
                placeholder="••••••••"
              />
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
              Confirm Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
              </div>
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                name="confirmPassword"
                type="password"
                required
                class="pl-10 w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm"
                placeholder="••••••••"
              />
            </div>
          </div>

          <!-- Terms checkbox -->
          <div class="flex items-start">
            <div class="flex items-center h-5">
              <input
                id="agree-terms"
                v-model="form.agreeTerms"
                name="agree-terms"
                type="checkbox"
                required
                class="h-4 w-4 text-primary-400 focus:ring-primary-400 border-gray-300 rounded"
              />
            </div>
            <div class="ml-3 text-sm">
              <label for="agree-terms" class="text-gray-600">
                I agree to the
                <NuxtLink to="/terms" class="text-primary-100 hover:text-primary-200 font-medium" target="_blank">Terms and Conditions</NuxtLink>
                and
                <NuxtLink to="/terms" class="text-primary-100 hover:text-primary-200 font-medium" target="_blank">Privacy Policy</NuxtLink>
              </label>
            </div>
          </div>

          <!-- Submit button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center items-center px-4 py-3 bg-gradient-to-r from-primary-300 via-primary-400 to-primary-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Creating your account...' : 'Create Account' }}
          </button>

          <!-- Error message -->
          <div v-if="error || authError" class="rounded-xl bg-red-50 border border-red-200 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-red-800">
                  {{ error || authError }}
                </p>
              </div>
            </div>
          </div>

          <!-- Success message -->
          <div v-if="success" class="rounded-xl bg-green-50 border border-green-200 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-green-800">
                  {{ success }}
                </p>
              </div>
            </div>
          </div>
        </form>

        <!-- Login link -->
        <div class="mt-8 text-center">
          <p class="text-sm text-gray-600">
            Already have an account?
            <NuxtLink to="/login" class="font-medium text-primary-100 hover:text-primary-200 transition-colors">
              Sign in here
            </NuxtLink>
          </p>
          <p class="text-sm text-gray-600 mt-2">
            <NuxtLink to="/about" class="font-medium text-primary-100 hover:text-primary-200 transition-colors">
              Learn more about ComKit
            </NuxtLink>
          </p>
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
  title: 'Register - ComKit',
  description: 'Create a new ComKit account',
  middleware: guestMiddleware,
})

// Form data interface
interface RegisterForm {
  username: string
  name: string
  address: string
  password: string
  confirmPassword: string
  agreeTerms: boolean
}

// Form data
const form = ref<RegisterForm>({
  username: '',
  name: '',
  address: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

// Use auth composable
const { register, isLoading, error: authError } = useAuth()

// State
const loading = isLoading
const error = ref<string>('')
const success = ref<string>('')

// Methods
const validateForm = (): boolean => {
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return false
  }

  if (form.value.password.length < 6) {
    error.value = 'Password must be at least 6 characters long'
    return false
  }

  if (!form.value.agreeTerms) {
    error.value = 'You must agree to the terms and conditions'
    return false
  }

  return true
}

const handleRegister = async (): Promise<void> => {
  error.value = ''
  success.value = ''

  if (!validateForm()) {
    return
  }

  try {
    await register({
      username: form.value.username,
      name: form.value.name,
      address: form.value.address,
      password: form.value.password
    })
    
    // Registration successful - redirect to dashboard (user is auto-logged in)
    success.value = 'Account created successfully! Redirecting to dashboard...'
    await navigateTo('/dashboard')
  } catch (err: any) {
    // Error is already handled by the auth composable
    console.error('Registration error:', err)
  }
}
</script>

<style scoped>
/* Custom animations and transitions */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* Glassmorphism effect */
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Pattern overlay */
.pattern-overlay {
  background-image: url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.4"%3E%3Cpath d="M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.mobile-container {
  max-width: 375px;
  margin: 0 auto;
}
</style>