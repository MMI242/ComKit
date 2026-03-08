// API base configuration
let API_BASE_URL: string
let AUTH_TOKEN: string | null = null

// Function to initialize API base URL (call this in plugin or middleware)
export const initApi = (baseURL: string) => {
  API_BASE_URL = baseURL
}

// Function to set auth token (for fallback authentication)
export const setAuthToken = (token: string) => {
  AUTH_TOKEN = token
}

// Function to get auth token
export const getAuthToken = () => AUTH_TOKEN

// Types for API responses
export interface LoginRequest {
  username: string
  password: string
}

export interface SetAuthCookiesRequest {
  access_token: string
  refresh_token: string
  remember_me: boolean
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

// Item types
export interface ItemOwner {
  id: number
  username: string
  name: string
  address: string
}

export interface Item {
  id: number
  name: string
  description: string
  qty: number
  remaining_qty: number
  unit: string
  thumbnail_url?: string
  photo_url?: string
  type: 'borrow' | 'share'
  status: 'available' | 'borrowed'
  owner: ItemOwner
}

// AI Recipe types
export interface RecipeRequest {
  ingredients: string
}

export interface RecipeResponse {
  recipe: {
    title: string
    ingredients: string[]
    instructions: string[]
    cooking_time: string
    servings: string
    difficulty: string
    raw_text?: string
  }
  generated_at: string
}

export interface Pagination {
  current_page: number
  total_pages: number
  total_items: number
  items_per_page: number
}

export interface ItemsResponse {
  items: Item[]
  pagination: Pagination
}

export interface RequestItemRequest {
  requested_qty: number
  date_start: string
  date_end: string
}

export interface RequestItemResponse {
  request_id: number
  item: {
    id: number
    name: string
    unit: string
  }
  requested_qty: number
  date_start: string
  date_end: string
  status: string
  requester: {
    id: number
    username: string
    name: string
  }
  created_at: string
}

// User Items types
export interface UserItem {
  id: number
  name: string
  description: string
  qty: number
  remaining_qty: number
  unit: string
  thumbnail_url?: string
  photo_url?: string
  type: 'borrow' | 'share'
  status: 'available' | 'borrowed'
  created_at: string
  updated_at: string
}

export interface UserItemListResponse {
  items: UserItem[]
}

export interface UserItemCreate {
  name: string
  description: string
  qty: number
  unit: string
  type: 'borrow' | 'share'
  status: 'available' | 'borrowed'
  photo?: File
}

export interface UserItemUpdate {
  name: string
  description: string
  qty: number
  unit: string
  type: 'borrow' | 'share'
  status: 'available' | 'borrowed'
  photo?: File
}

// User Requests types
export interface RequestItemInfo {
  id: number
  name: string
  thumbnail_url?: string
  unit: string
}

export interface RequestUser {
  id: number
  username: string
  name: string
  address: string
}

export interface RequestResponse {
  id: number
  item: RequestItemInfo
  requester?: RequestUser
  owner?: RequestUser
  requested_qty: number
  unit: string
  date_start: string
  date_end: string
  status: 'pending' | 'approved' | 'rejected' | 'returned' | 'cancelled'
  created_at: string
  updated_at: string
}

export interface RequestListResponse {
  requests: RequestResponse[]
}

export interface RequestStatusUpdate {
  status: 'approved' | 'rejected' | 'returned' | 'cancelled'
}

// Generic API client
class ApiClient {
  private baseURL: string

  constructor(baseURL?: string) {
    this.baseURL = baseURL || API_BASE_URL || 'http://localhost:8000'
  }

  public async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const config: RequestInit = {
      credentials: 'include', // Include cookies in requests
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        // Handle 401 Unauthorized globally - redirect to login
        if (response.status === 401) {
          // Only redirect on client side to avoid SSR issues
          if (process.client) {
            await navigateTo('/login')
          }
          throw {
            detail: 'Authentication required. Redirecting to login...',
            status: 401
          } as ApiError
        }

        const errorData = await response.json().catch(() => ({ detail: 'Network error' }))
        throw {
          detail: errorData.detail || `HTTP ${response.status}`,
          status: response.status
        } as ApiError
      }

      const successData = await response.json() as T
      return successData
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

  async postWithAuth<T>(endpoint: string, data?: any): Promise<T> {
    
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
      credentials: 'include', // This will include cookies automatically
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

  async getWithAuth<T>(endpoint: string): Promise<T> {
    const headers: Record<string, string> = {}
    
    // Try to get token from memory first (fallback)
    if (AUTH_TOKEN) {
      headers['Authorization'] = `Bearer ${AUTH_TOKEN}`
    }
    
    return this.request<T>(endpoint, {
      method: 'GET',
      headers,
    })
  }
}

// Create API client instance
const apiClient = new ApiClient()

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
  },

  async clearAuthCookies(): Promise<void> {
    // This endpoint should clear HTTP-only cookies on the server
    return apiClient.post<void>('/auth/clear-cookies')
  },

  async validateCookies(): Promise<AuthResponse> {
    // This endpoint should validate HTTP-only cookies and return auth data
    return apiClient.get<AuthResponse>('/auth/validate-cookies')
  }
}

// Items API service
export const itemsApi = {
  async getItems(
    page: number = 1,
    search: string = '',
    type: string = 'all'
  ): Promise<ItemsResponse> {
    const params = new URLSearchParams({
      page: page.toString(),
      search: search,
      type: type
    })
    
    return apiClient.getWithAuth<ItemsResponse>(`/items?${params.toString()}`)
  },

  async requestItem(
    itemId: number,
    requestData: RequestItemRequest
  ): Promise<RequestItemResponse> {
    return apiClient.postWithAuth<RequestItemResponse>(`/items/${itemId}/request`, requestData)
  }
}

// AI API service
export const aiApi = {
  async generateRecipe(request: RecipeRequest): Promise<RecipeResponse> {
    return apiClient.postWithAuth<RecipeResponse>('/ai/recipe', request)
  }
}

// User Items API service
export const userItemsApi = {
  async getUserItems(): Promise<UserItemListResponse> {
    return apiClient.getWithAuth<UserItemListResponse>('/user/items')
  },

  async createUserItem(formData: FormData): Promise<UserItem> {
    const headers: Record<string, string> = {}
    
    // Try to get token from memory first (fallback)
    if (AUTH_TOKEN) {
      headers['Authorization'] = `Bearer ${AUTH_TOKEN}`
    }

    return apiClient.request<UserItem>('/user/items', {
      method: 'POST',
      headers,
      body: formData,
      credentials: 'include',
    })
  },

  async updateUserItem(itemId: number, formData: FormData): Promise<UserItem> {
    const headers: Record<string, string> = {}
    
    // Try to get token from memory first (fallback)
    if (AUTH_TOKEN) {
      headers['Authorization'] = `Bearer ${AUTH_TOKEN}`
    }

    return apiClient.request<UserItem>(`/user/items/${itemId}`, {
      method: 'PUT',
      headers,
      body: formData,
      credentials: 'include',
    })
  },

  async deleteUserItem(itemId: number): Promise<{ message: string; item_id: number }> {
    const headers: Record<string, string> = {}
    
    // Try to get token from memory first (fallback)
    if (AUTH_TOKEN) {
      headers['Authorization'] = `Bearer ${AUTH_TOKEN}`
    }

    return apiClient.request<{ message: string; item_id: number }>(`/user/items/${itemId}`, {
      method: 'DELETE',
      headers,
      credentials: 'include',
    })
  }
}

// User Requests API service
export const userRequestsApi = {
  async getUserRequests(type: 'incoming' | 'outgoing'): Promise<RequestListResponse> {
    const params = new URLSearchParams({
      type: type
    })
    
    return apiClient.getWithAuth<RequestListResponse>(`/user/requests?${params.toString()}`)
  },

  async updateRequestStatus(
    requestId: number,
    statusUpdate: RequestStatusUpdate
  ): Promise<RequestResponse> {
    return apiClient.request<RequestResponse>(`/user/requests/${requestId}`, {
      method: 'PATCH',
      body: JSON.stringify(statusUpdate),
      credentials: 'include',
    })
  }
}

export default apiClient
