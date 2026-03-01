import { ref, computed, readonly } from 'vue'
import type { AuthResponse, ApiError } from '../services/api'

// Auth state
const user = ref<AuthResponse['user'] | null>(null)
const accessToken = ref<string | null>(null)
const refreshToken = ref<string | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)

// Load auth state from localStorage on client side
const loadAuthState = () => {
  if (process.client) {
    const storedUser = localStorage.getItem('auth_user')
    const storedAccessToken = localStorage.getItem('auth_access_token')
    const storedRefreshToken = localStorage.getItem('auth_refresh_token')
    
    if (storedUser) user.value = JSON.parse(storedUser)
    if (storedAccessToken) accessToken.value = storedAccessToken
    if (storedRefreshToken) refreshToken.value = storedRefreshToken
  }
}

// Save auth state to localStorage
const saveAuthState = (authData: AuthResponse, rememberMe: boolean = false) => {
  user.value = authData.user
  accessToken.value = authData.access_token
  refreshToken.value = authData.refresh_token
  
  if (process.client) {
    if (rememberMe) {
      localStorage.setItem('auth_user', JSON.stringify(authData.user))
      localStorage.setItem('auth_access_token', authData.access_token)
      localStorage.setItem('auth_refresh_token', authData.refresh_token)
    } else {
      // Use sessionStorage for "remember me" = false
      sessionStorage.setItem('auth_user', JSON.stringify(authData.user))
      sessionStorage.setItem('auth_access_token', authData.access_token)
      sessionStorage.setItem('auth_refresh_token', authData.refresh_token)
    }
  }
}

// Clear auth state
const clearAuthState = () => {
  user.value = null
  accessToken.value = null
  refreshToken.value = null
  error.value = null
  
  if (process.client) {
    localStorage.removeItem('auth_user')
    localStorage.removeItem('auth_access_token')
    localStorage.removeItem('auth_refresh_token')
    sessionStorage.removeItem('auth_user')
    sessionStorage.removeItem('auth_access_token')
    sessionStorage.removeItem('auth_refresh_token')
  }
}

// Composable for authentication
export const useAuth = () => {
  // Computed properties
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const currentUser = computed(() => user.value)
  
  // Login method
  const login = async (username: string, password: string, rememberMe: boolean = false) => {
    isLoading.value = true
    error.value = null
    
    try {
      const { authApi } = await import('../services/api')
      const response = await authApi.login({ username, password })
      
      saveAuthState(response, rememberMe)
      
      return response
    } catch (err) {
      const apiError = err as ApiError
      error.value = apiError.detail || 'Login failed'
      throw apiError
    } finally {
      isLoading.value = false
    }
  }
  
  // Register method
  const register = async (userData: {
    username: string
    password: string
    name: string
    address: string
  }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const { authApi } = await import('../services/api')
      const response = await authApi.register(userData)
      
      // Auto-login after registration
      saveAuthState(response, true)
      
      return response
    } catch (err) {
      const apiError = err as ApiError
      error.value = apiError.detail || 'Registration failed'
      throw apiError
    } finally {
      isLoading.value = false
    }
  }
  
  // Logout method
  const logout = () => {
    clearAuthState()
    // Navigate to login page
    navigateTo('/login')
  }
  
  // Initialize auth state
  const initAuth = () => {
    loadAuthState()
  }
  
  return {
    // State
    user: readonly(user),
    accessToken: readonly(accessToken),
    isLoading: readonly(isLoading),
    error: readonly(error),
    
    // Computed
    isAuthenticated,
    currentUser,
    
    // Methods
    login,
    register,
    logout,
    initAuth
  }
}

// Initialize auth state on app startup
if (process.client) {
  const auth = useAuth()
  auth.initAuth()
}
