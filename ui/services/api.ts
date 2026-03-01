// API base configuration
const config = useRuntimeConfig()
const API_BASE_URL = config.public.apiBase

// Types for API responses
export interface LoginRequest {
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: {
    id: number
    username: string
    name: string
    address: string
  }
}

export interface ApiError {
  detail: string
  status?: number
}

// Generic API client
class ApiClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Network error' }))
        throw {
          detail: errorData.detail || `HTTP ${response.status}`,
          status: response.status
        } as ApiError
      }

      return await response.json() as T
    } catch (error) {
      if (error instanceof TypeError) {
        throw { detail: 'Network error. Please check your connection.' } as ApiError
      }
      throw error
    }
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async get<T>(endpoint: string, token?: string): Promise<T> {
    const headers: Record<string, string> = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    return this.request<T>(endpoint, {
      method: 'GET',
      headers,
    })
  }
}

// Create API client instance
const apiClient = new ApiClient(API_BASE_URL)

// Auth API service
export const authApi = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    return apiClient.post<AuthResponse>('/auth/login', credentials)
  },

  async register(userData: {
    username: string
    password: string
    name: string
    address: string
  }): Promise<AuthResponse> {
    return apiClient.post<AuthResponse>('/auth/register', userData)
  },

  async refreshToken(refreshToken: string): Promise<{
    access_token: string
    token_type: string
    expires_in: number
  }> {
    return apiClient.post('/auth/refresh', { refresh_token: refreshToken })
  }
}

export default apiClient
