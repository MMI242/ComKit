<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Create your account
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          <NuxtLink to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
            sign in to your existing account
          </NuxtLink>
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="username" class="form-label">Username</label>
            <input
              id="username"
              v-model="form.username"
              name="username"
              type="text"
              required
              class="input-field"
              placeholder="Choose a username"
            />
          </div>

          <div>
            <label for="name" class="form-label">Full Name</label>
            <input
              id="name"
              v-model="form.name"
              name="name"
              type="text"
              required
              class="input-field"
              placeholder="Enter your full name"
            />
          </div>

          <div>
            <label for="address" class="form-label">Address</label>
            <textarea
              id="address"
              v-model="form.address"
              name="address"
              rows="3"
              required
              class="input-field"
              placeholder="Enter your address"
            />
          </div>

          <div>
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="input-field"
              placeholder="Create a password"
            />
          </div>

          <div>
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              name="confirmPassword"
              type="password"
              required
              class="input-field"
              placeholder="Confirm your password"
            />
          </div>
        </div>

        <div class="flex items-center">
          <input
            id="agree-terms"
            v-model="form.agreeTerms"
            name="agree-terms"
            type="checkbox"
            required
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label for="agree-terms" class="ml-2 block text-sm text-gray-900">
            I agree to the
            <a href="#" class="text-indigo-600 hover:text-indigo-500">Terms of Service</a>
            and
            <a href="#" class="text-indigo-600 hover:text-indigo-500">Privacy Policy</a>
          </label>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="btn-primary w-full flex justify-center items-center disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg
                class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"
                />
              </svg>
            </span>
            {{ loading ? 'Creating account...' : 'Create account' }}
          </button>
        </div>

        <div v-if="error || authError" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg
                class="h-5 w-5 text-red-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">
                {{ error || authError }}
              </h3>
            </div>
          </div>
        </div>

        <div v-if="success" class="rounded-md bg-green-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg
                class="h-5 w-5 text-green-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-green-800">
                {{ success }}
              </h3>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../../composables/useAuth'

// Page metadata
definePageMeta({
  title: 'Register - ComKit',
  description: 'Create a new ComKit account'
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
    
    // Registration successful - redirect to login
    success.value = 'Account created successfully! Redirecting to login...'
    await navigateTo('/login')
  } catch (err: any) {
    // Error is already handled by the auth composable
    console.error('Registration error:', err)
  }
}
</script>

<style scoped>
/* Additional styles if needed */
</style>
