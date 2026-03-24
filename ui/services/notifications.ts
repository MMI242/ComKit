import { ref, computed } from 'vue'
import { getAuthToken } from './api'

export interface Notification {
  type: string
  data: {
    request_id?: number
    item_name?: string
    requester_name?: string
    owner_name?: string
    status?: string
    notification_type?: string
    requested_qty?: number
    unit?: string
    user_id?: number
    message?: string
  }
  timestamp: string
}

class NotificationService {
  private socket: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private pingInterval: NodeJS.Timeout | null = null
  private isConnecting = false
  private notificationsEnabled: boolean

  // Reactive state
  public isConnected = ref(false)
  public notifications = ref<Notification[]>([])
  public unreadCount = ref(0)

  constructor() {
    // Check if notifications are enabled via environment
    this.notificationsEnabled = this.getNotificationsEnabled()
    
    // Auto-connect when token is available and notifications are enabled
    if (process.client && getAuthToken() && this.notificationsEnabled) {
      this.connect()
    }
  }

  private getNotificationsEnabled(): boolean {
    // Check runtime config first, then fallback to environment
    if (process.client && typeof window !== 'undefined') {
      // @ts-ignore
      const config = window.__NUXT__?.config?.public
      if (config?.enableNotifications !== undefined) {
        return config.enableNotifications === true
      }
    }
    
    // Fallback to enabled by default
    return true
  }

  private getWebSocketUrl(userId: number): string {
    const baseURL = this.getApiBaseUrl()
    const token = getAuthToken()
    return `${baseURL.replace('http', 'ws')}/ws/notifications/${userId}?token=${token}`
  }

  private getApiBaseUrl(): string {
    if (process.server) return 'ws://localhost:8000'
    
    // Try to determine the base URL similar to API service
    if (typeof window !== 'undefined') {
      const port = window.location.port
      if (port === '17999') {
        return `${window.location.protocol}//${window.location.hostname}:18000`
      }
      if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        return `${window.location.protocol}//${window.location.hostname}:18000`
      }
    }
    
    return 'ws://localhost:8000'
  }

  public async connect(userId?: number): Promise<void> {
    if (!this.notificationsEnabled) {
      console.log('Notifications are disabled, skipping WebSocket connection')
      return
    }
    
    if (this.isConnecting || this.socket?.readyState === WebSocket.OPEN) {
      return
    }

    this.isConnecting = true
    
    try {
      const token = getAuthToken()
      if (!token) {
        console.warn('No auth token available for WebSocket connection')
        this.isConnecting = false
        return
      }

      // Get user ID from token or parameter
      let targetUserId: number | undefined = userId
      if (targetUserId === undefined) {
        // Decode JWT to get user ID (simple parsing)
        try {
          // Validate token format first
          const tokenParts = token.split('.')
          if (tokenParts.length !== 3) {
            throw new Error('Invalid token format')
          }
          
          const base64Payload = tokenParts[1]
          if (!base64Payload) {
            throw new Error('No payload found in token')
          }
          
          // Universal base64 decoding approach
          let payload: any
          
          if (typeof window !== 'undefined' && window.atob) {
            // Browser environment - use window.atob
            const binaryString = window.atob(base64Payload)
            payload = JSON.parse(binaryString)
          } else if (typeof Buffer !== 'undefined') {
            // Node.js environment - use Buffer
            const buffer = Buffer.from(base64Payload, 'base64')
            payload = JSON.parse(buffer.toString('utf8'))
          } else {
            // Fallback - try to use atob (might be available globally)
            const binaryString = (globalThis as any).atob?.(base64Payload)
            if (binaryString) {
              payload = JSON.parse(binaryString)
            } else {
              throw new Error('No base64 decoding method available')
            }
          }
          
          targetUserId = payload.user_id as number
        } catch (e) {
          console.error('Failed to decode user ID from token', e)
          this.isConnecting = false
          return
        }
      }

      // Ensure we have a valid user ID
      if (targetUserId === undefined || targetUserId === null) {
        console.error('No valid user ID available for WebSocket connection')
        this.isConnecting = false
        return
      }

      const wsUrl = this.getWebSocketUrl(targetUserId)
      console.log('Connecting to WebSocket:', wsUrl)

      this.socket = new WebSocket(wsUrl)

      this.socket.onopen = () => {
        console.log('WebSocket connected')
        this.isConnected.value = true
        this.isConnecting = false
        this.reconnectAttempts = 0
        this.startPing()
      }

      this.socket.onmessage = (event) => {
        try {
          const notification: Notification = JSON.parse(event.data)
          this.handleNotification(notification)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      this.socket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason)
        this.isConnected.value = false
        this.isConnecting = false
        this.stopPing()
        
        // Attempt reconnection if not a normal closure
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
          setTimeout(() => {
            this.reconnectAttempts++
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
            this.connect(targetUserId)
          }, this.reconnectDelay * this.reconnectAttempts)
        }
      }

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.isConnected.value = false
        this.isConnecting = false
      }

    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
      this.isConnecting = false
    }
  }

  public disconnect(): void {
    this.stopPing()
    if (this.socket) {
      this.socket.close(1000, 'User disconnected')
      this.socket = null
    }
    this.isConnected.value = false
  }

  private handleNotification(notification: Notification): void {
    console.log('Received notification:', notification)
    
    // Add to notifications list
    this.notifications.value.unshift(notification)
    
    // Keep only last 50 notifications
    if (this.notifications.value.length > 50) {
      this.notifications.value = this.notifications.value.slice(0, 50)
    }
    
    // Increment unread count
    this.unreadCount.value++
    
    // Show browser notification if permission granted
    this.showBrowserNotification(notification)
  }

  private showBrowserNotification(notification: Notification): void {
    if (!('Notification' in window)) return
    
    if (Notification.permission === 'granted') {
      const title = this.getNotificationTitle(notification)
      const body = this.getNotificationBody(notification)
      
      new Notification(title, {
        body,
        icon: '/favicon.ico',
        tag: `notification-${notification.type}`
      })
    } else if (Notification.permission !== 'denied') {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          this.showBrowserNotification(notification)
        }
      })
    }
  }

  private getNotificationTitle(notification: Notification): string {
    switch (notification.type) {
      case 'new_request':
        return 'New Request Received'
      case 'request_update':
        return 'Request Status Updated'
      case 'connection_established':
        return 'Connected'
      default:
        return 'ComKit Notification'
    }
  }

  private getNotificationBody(notification: Notification): string {
    const { data } = notification
    
    switch (notification.type) {
      case 'new_request':
        return `${data.requester_name} requested ${data.requested_qty} ${data.unit} of ${data.item_name}`
      case 'request_update':
        if (data.status === 'approved') {
          return `Your request for ${data.item_name} has been approved!`
        } else if (data.status === 'rejected') {
          return `Your request for ${data.item_name} has been rejected`
        } else if (data.status === 'returned') {
          return `Request for ${data.item_name} marked as returned`
        } else if (data.status === 'cancelled') {
          return `Request for ${data.item_name} has been cancelled`
        }
        return `Request for ${data.item_name} updated to ${data.status}`
      case 'connection_established':
        return data.message || 'Connected to notification service'
      default:
        return 'You have a new notification'
    }
  }

  private startPing(): void {
    this.stopPing()
    this.pingInterval = setInterval(() => {
      if (this.socket?.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify({ type: 'ping', timestamp: Date.now() }))
      }
    }, 30000) // Ping every 30 seconds
  }

  private stopPing(): void {
    if (this.pingInterval) {
      clearInterval(this.pingInterval)
      this.pingInterval = null
    }
  }

  public markAsRead(notificationId?: number): void {
    if (notificationId) {
      const notification = this.notifications.value.find(n => 
        n.data.request_id === notificationId
      )
      if (notification) {
        // Mark specific notification as read (implementation depends on your needs)
      }
    } else {
      // Mark all as read
      this.unreadCount.value = 0
    }
  }

  public clearNotifications(): void {
    this.notifications.value = []
    this.unreadCount.value = 0
  }

  // Computed properties
  public recentNotifications = computed(() => 
    this.notifications.value.slice(0, 10)
  )

  public hasUnread = computed(() => 
    this.unreadCount.value > 0
  )
}

// Create singleton instance
export const notificationService = new NotificationService()

// Export as composable for Vue
export function useNotifications() {
  return {
    isConnected: notificationService.isConnected,
    notifications: notificationService.notifications,
    unreadCount: notificationService.unreadCount,
    recentNotifications: notificationService.recentNotifications,
    hasUnread: notificationService.hasUnread,
    connect: notificationService.connect.bind(notificationService),
    disconnect: notificationService.disconnect.bind(notificationService),
    markAsRead: notificationService.markAsRead.bind(notificationService),
    clearNotifications: notificationService.clearNotifications.bind(notificationService)
  }
}
