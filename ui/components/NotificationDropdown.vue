<template>
  <div v-if="isNotificationsEnabled" class="relative">
    <!-- Notification Bell Icon -->
    <button
      @click="toggleDropdown"
      class="relative p-2 text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-full"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      
      <!-- Unread Badge -->
      <span
        v-if="hasUnread"
        class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-600 rounded-full transform translate-x-1 -translate-y-1"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <!-- Notification Dropdown -->
    <div
      v-if="showDropdown"
      class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg z-50 max-h-96 overflow-hidden"
    >
      <!-- Header -->
      <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between">
        <h3 class="text-sm font-medium text-gray-900">Notifications</h3>
        <button
          v-if="hasUnread"
          @click="markAllAsRead"
          class="text-xs text-primary-600 hover:text-primary-800"
        >
          Mark all as read
        </button>
      </div>

      <!-- Notifications List -->
      <div class="max-h-80 overflow-y-auto">
        <div v-if="recentNotifications.length === 0" class="px-4 py-8 text-center text-gray-500">
          <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <p class="text-sm">No notifications yet</p>
        </div>

        <div v-else>
          <div
            v-for="notification in recentNotifications"
            :key="getNotificationKey(notification)"
            class="px-4 py-3 hover:bg-gray-50 border-b border-gray-100 cursor-pointer transition-colors"
            @click="handleNotificationClick(notification)"
          >
            <div class="flex items-start">
              <!-- Icon -->
              <div class="flex-shrink-0 mr-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center"
                     :class="getNotificationIconClass(notification)">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path :d="getNotificationIconPath(notification)" />
                  </svg>
                </div>
              </div>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <p class="text-sm text-gray-900 font-medium">
                  {{ getNotificationTitle(notification) }}
                </p>
                <p class="text-sm text-gray-600 mt-1">
                  {{ getNotificationMessage(notification) }}
                </p>
                <p class="text-xs text-gray-400 mt-1">
                  {{ formatTimestamp(notification.timestamp) }}
                </p>
              </div>

              <!-- Unread Indicator -->
              <div v-if="isUnread(notification)" class="flex-shrink-0 ml-2">
                <div class="w-2 h-2 bg-primary-600 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-4 py-2 border-t border-gray-200">
        <button
          @click="clearAllNotifications"
          class="w-full text-center text-sm text-gray-600 hover:text-gray-900"
        >
          Clear all notifications
        </button>
      </div>
    </div>

    <!-- Overlay -->
    <div
      v-if="showDropdown && isNotificationsEnabled"
      @click="closeDropdown"
      class="fixed inset-0 z-40"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useNotifications, type Notification } from '~~/services/notifications'
import { useRuntimeConfig } from '#app'

const {
  notifications,
  unreadCount,
  recentNotifications,
  hasUnread,
  markAsRead,
  clearNotifications
} = useNotifications()

const config = useRuntimeConfig()

// Check if notifications are enabled
const isNotificationsEnabled = computed(() => {
  console.log('NotificationDropdown - Nuxt runtime config:', config.public)
  console.log('NotificationDropdown - enableNotifications value:', config.public.enableNotifications)
  
  // Use the runtime config directly
  if (config.public.enableNotifications !== undefined) {
    return config.public.enableNotifications === true
  }
  
  // Fallback to enabled by default
  console.log('NotificationDropdown - Using default (enabled)')
  return true
})

const showDropdown = ref(false)

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const closeDropdown = () => {
  showDropdown.value = false
}

const markAllAsRead = () => {
  markAsRead()
}

const clearAllNotifications = () => {
  clearNotifications()
  closeDropdown()
}

const handleNotificationClick = (notification: Notification) => {
  // Mark as read and handle navigation if needed
  const data = notification.data || {}
  const requestId = data.request_id
  if (requestId) {
    markAsRead(requestId)
  }
  
  // Navigate to relevant page based on notification type
  if (notification.type === 'new_request' || notification.type === 'request_update') {
    navigateTo('/mypage')
  }
  
  closeDropdown()
}

const getNotificationKey = (notification: Notification): string => {
  const data = notification.data || {}
  const requestId = data.request_id
  const timestamp = notification.timestamp
  return `${notification.type}-${requestId || timestamp || Date.now()}`
}

const getNotificationTitle = (notification: Notification): string => {
  switch (notification.type) {
    case 'new_request':
      return 'New Request Received'
    case 'request_update':
      return 'Request Status Updated'
    case 'connection_established':
      return 'Connected'
    default:
      return 'Notification'
  }
}

const getNotificationMessage = (notification: Notification): string => {
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

const getNotificationIconClass = (notification: Notification): string => {
  switch (notification.type) {
    case 'new_request':
      return 'bg-blue-100 text-blue-600'
    case 'request_update':
      if (notification.data.status === 'approved') {
        return 'bg-green-100 text-green-600'
      } else if (notification.data.status === 'rejected') {
        return 'bg-red-100 text-red-600'
      }
      return 'bg-yellow-100 text-yellow-600'
    default:
      return 'bg-gray-100 text-gray-600'
  }
}

const getNotificationIconPath = (notification: Notification): string => {
  switch (notification.type) {
    case 'new_request':
      return 'M18 9a3 3 0 11-6 0 3 3 0 016 0zm-3 4a5 5 0 00-5 5v1H10v-1a5 5 0 00-5-5h14z'
    case 'request_update':
      if (notification.data.status === 'approved') {
        return 'M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z'
      } else if (notification.data.status === 'rejected') {
        return 'M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z'
      }
      return 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
    default:
      return 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
  }
}

const isUnread = (notification: Notification): boolean => {
  // Simple logic: consider all notifications as unread for now
  // In a real app, you'd track read status
  return false
}

const formatTimestamp = (timestamp: string): string => {
  try {
    let date: Date
    
    // Handle different timestamp formats
    if (timestamp.includes('$date')) {
      // MongoDB-style timestamp
      const parsed = JSON.parse(timestamp)
      date = new Date(parsed.$date.$numberLong)
    } else if (!isNaN(Number(timestamp))) {
      // Unix timestamp number
      date = new Date(Number(timestamp))
    } else {
      // ISO string or other format
      date = new Date(timestamp)
    }
    
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours}h ago`
    
    const diffDays = Math.floor(diffHours / 24)
    if (diffDays < 7) return `${diffDays}d ago`
    
    return date.toLocaleDateString()
  } catch {
    return 'Unknown time'
  }
}

// Close dropdown when clicking outside
if (process.client) {
  document.addEventListener('click', (e) => {
    const target = e.target as HTMLElement
    if (!target.closest('.relative')) {
      showDropdown.value = false
    }
  })
}
</script>

<style scoped>
/* Custom scrollbar for notifications list */
.max-h-80::-webkit-scrollbar {
  width: 4px;
}

.max-h-80::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.max-h-80::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.max-h-80::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
