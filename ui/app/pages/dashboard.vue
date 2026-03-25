<template>
  <div class="min-h-screen bg-gray-50 mobile-container">
    <TopHeader :user="user" :is-logging-out="isLoggingOut" @logout="handleLogout" />

    <!-- Main content -->
    <main class="pt-12 pb-16 px-4">
      <div class="py-4">
        <!-- Search and Filter Section -->
        <div class="mb-6 bg-white p-4 rounded-lg shadow">
          <div class="flex flex-col gap-4">
            <div class="flex-1">
              <input
                v-model="searchQuery"
                @input="handleSearch"
                type="text"
                :placeholder="$t('dashboard.search_placeholder')"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div class="flex gap-2 flex-wrap">
              <label class="flex items-center">
                <input
                  v-model="filterType"
                  @change="handleFilter"
                  type="radio"
                  value="all"
                  class="mr-2"
                />
                <span class="text-sm">{{ $t('dashboard.filter_all') }}</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="filterType"
                  @change="handleFilter"
                  type="radio"
                  value="borrow"
                  class="mr-2"
                />
                <span class="text-sm">{{ $t('dashboard.filter_borrow') }}</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="filterType"
                  @change="handleFilter"
                  type="radio"
                  value="share"
                  class="mr-2"
                />
                <span class="text-sm">{{ $t('dashboard.filter_share') }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {{ error }}
        </div>

        <!-- Items List -->
        <div class="space-y-4">
          <div v-if="loading" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p class="text-gray-600">{{ $t('dashboard.loading_items') }}</p>
          </div>

          <div v-else-if="items.length === 0" class="text-center py-8 bg-white rounded-lg shadow">
            <p class="text-gray-600">{{ $t('dashboard.no_items_found') }}</p>
          </div>

          <div v-else>
            <div
              v-for="item in items"
              :key="item.id"
              class="bg-white rounded-lg shadow overflow-hidden my-3"
            >
              <!-- Collapsed State -->
              <div v-if="!expandedItems.includes(item.id)" class="p-4">
                <div class="flex items-center space-x-4">
                  <img
                    :src="item.thumbnail_url || config.public.defaultPlaceholderImage"
                    :alt="item.name"
                    class="h-16 w-16 object-cover rounded-lg"
                  />
                  <div class="flex-1">
                    <h3 class="text-lg font-medium text-gray-900">{{ item.name }}</h3>
                    <p class="text-sm text-gray-600">{{ $t('dashboard.owner') }}: {{ item.owner.name }}</p>
                    <p class="text-sm text-gray-600">
                      {{ $t('dashboard.available') }}: {{ item.remaining_qty }}/{{ item.qty }} {{ item.unit }}
                    </p>
                    <span class="inline-flex items-center px-2.5 py-0.5 mt-3 rounded-full text-xs font-medium"
                          :class="item.type === 'borrow' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'">
                      {{ item.type === 'borrow' ? $t('dashboard.filter_borrow') : $t('dashboard.filter_share') }}
                    </span>
                  </div>
                  <button
                    @click="toggleExpand(item.id)"
                    class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    {{ $t('dashboard.details') }}
                  </button>
                </div>
              </div>

              <!-- Expanded State -->
              <div v-else class="p-4">
                <div class="mb-4">
                  <img
                    :src="item.photo_url || config.public.defaultPlaceholderImage"
                    :alt="item.name"
                    class="w-full h-48 object-cover rounded-lg"
                  />
                </div>

                <div class="space-y-2">
                  <h3 class="text-xl font-bold text-gray-900">{{ item.name }}</h3>
                  <p class="text-gray-700">{{ item.description }}</p>
                  <p class="text-sm text-gray-600">
                    <strong>{{ $t('dashboard.available') }}:</strong> {{ item.remaining_qty }}/{{ item.qty }} {{ item.unit }}
                  </p>
                  <p class="text-sm text-gray-600">
                    <strong>{{ $t('dashboard.owner') }}:</strong> {{ item.owner.name }}
                  </p>
                  <p class="text-sm text-gray-600">
                    <strong>{{ $t('dashboard.address') }}:</strong> {{ item.owner.address }}
                  </p>
                  <p class="text-sm text-gray-600">
                    <strong>{{ $t('dashboard.type') }}:</strong> {{ item.type }}
                  </p>
                  <p class="text-sm text-gray-600">
                    <strong>{{ $t('dashboard.status') }}:</strong>
                    <span :class="item.status === 'available' ? 'text-green-600' : 'text-red-600'">
                      {{ item.status }}
                    </span>
                  </p>
                </div>

                <div class="mt-4 flex space-x-2">
                  <button
                    v-if="item.status === 'available' && item.remaining_qty > 0"
                    @click="openRequestForm(item)"
                    class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    {{ $t('dashboard.request_item') }}
                  </button>
                  <button
                    @click="toggleExpand(item.id)"
                    class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500"
                  >
                    {{ $t('dashboard.collapse') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.total_pages > 1" class="mt-6 flex items-center justify-between bg-white px-4 py-3 rounded-lg shadow">
          <div class="flex items-center text-sm text-gray-700">
            <span>{{ $t('dashboard.page_info', { current: pagination.current_page, total: pagination.total_pages, items: pagination.total_items }) }}</span>
          </div>
          <div class="flex space-x-2">
            <button
              @click="goToPage(pagination.current_page - 1)"
              :disabled="pagination.current_page === 1"
              class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ $t('common.previous') }}
            </button>
            <button
              @click="goToPage(pagination.current_page + 1)"
              :disabled="pagination.current_page === pagination.total_pages"
              class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ $t('common.next') }}
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Request Form Modal -->
    <div v-if="showRequestModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-bold mb-4">{{ $t('dashboard.request_modal_title', { name: selectedItem?.name }) }}</h3>

        <!-- Error Message -->
        <div v-if="error" class="mb-4 bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded">
          {{ error }}
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('dashboard.quantity') }}</label>
            <input
              v-model.number="requestForm.requested_qty"
              type="number"
              min="1"
              :max="selectedItem?.remaining_qty"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
            />
            <p class="text-xs text-gray-500 mt-1">{{ $t('dashboard.max_available', { qty: selectedItem?.remaining_qty, unit: selectedItem?.unit }) }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('dashboard.start_date') }}</label>
            <input
              v-model="requestForm.date_start"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ selectedItem?.type === 'borrow' ? $t('dashboard.end_date') : $t('dashboard.pickup_date') }}
            </label>
            <input
              v-model="requestForm.date_end"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </div>

        <div class="mt-6 flex space-x-2">
          <button
            @click="submitRequest"
            :disabled="submittingRequest"
            class="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
          >
            {{ submittingRequest ? $t('dashboard.submitting') : $t('dashboard.send_request') }}
          </button>
          <button
            @click="closeRequestForm"
            class="flex-1 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            {{ $t('common.cancel') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Bottom Navigation -->
    <BottomNavigation />

    <AuthLoadingOverlay :is-authenticating="isAuthenticating" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuth } from "~~/composables/useAuth"
import { itemsApi, type Item, type Pagination, type RequestItemRequest } from "~~/services/api"
import AuthLoadingOverlay from "~~/components/AuthLoadingOverlay.vue"
import BottomNavigation from '~~/components/BottomNavigation.vue'
import TopHeader from '~~/components/TopHeader.vue'

const config = useRuntimeConfig()

// Page metadata
definePageMeta({
  title: 'Dashboard - ComKit',
  description: 'Community items feed'
})

// Use auth composable
const { user: authUser, logout } = useAuth()

// Computed user data from auth
const user = computed(() => authUser.value || { name: 'User', username: 'user' })

// State
const items = ref<Item[]>([])
const pagination = ref<Pagination>({
  current_page: 1,
  total_pages: 1,
  total_items: 0,
  items_per_page: 25
})
const loading = ref(false)
const searchQuery = ref('')
const filterType = ref<'all' | 'borrow' | 'share'>('all')
const expandedItems = ref<number[]>([])
const showRequestModal = ref(false)
const selectedItem = ref<Item | null>(null)
const submittingRequest = ref(false)
const isLoggingOut = ref(false)
const error = ref<string>('')
const isAuthenticating = ref(false)

const requestForm = ref<RequestItemRequest>({
  requested_qty: 1,
  date_start: '',
  date_end: ''
})

// Methods
const loadItems = async (page: number = 1, search: string = '', type: string = 'all'): Promise<void> => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await itemsApi.getItems(page, search, type)
    
    items.value = response.items
    pagination.value = response.pagination
    
  } catch (err: any) {
    console.error('Error loading items:', err)
    error.value = $t('errors.failed_to_load_items')
  } finally {
    loading.value = false
  }
}

const handleSearch = (): void => {
  // Debounced search - implement debounce in real app
  setTimeout(() => {
    loadItems(1, searchQuery.value, filterType.value)
  }, 300)
}

const handleFilter = (): void => {
  loadItems(1, searchQuery.value, filterType.value)
}

const toggleExpand = (itemId: number): void => {
  const index = expandedItems.value.indexOf(itemId)
  if (index > -1) {
    expandedItems.value.splice(index, 1)
  } else {
    expandedItems.value.push(itemId)
  }
}

const openRequestForm = (item: Item): void => {
  selectedItem.value = item
  requestForm.value = {
    requested_qty: 1,
    date_start: '',
    date_end: ''
  }
  showRequestModal.value = true
}

const closeRequestForm = (): void => {
  showRequestModal.value = false
  selectedItem.value = null
  requestForm.value = {
    requested_qty: 1,
    date_start: '',
    date_end: ''
  }
}

const submitRequest = async (): Promise<void> => {
  if (!selectedItem.value) return
  
  // Validate form data
  if (!requestForm.value.date_start || !requestForm.value.date_end) {
    error.value = $t('errors.please_fill_dates')
    return
  }
  
  // Validate that end date is after start date
  if (requestForm.value.date_end < requestForm.value.date_start) {
    error.value = $t('errors.end_date_after_start')
    return
  }
  
  // Ensure data is properly formatted
  const requestData = {
    requested_qty: Number(requestForm.value.requested_qty),
    date_start: String(requestForm.value.date_start),
    date_end: String(requestForm.value.date_end)
  }
  
  try {
    submittingRequest.value = true
    error.value = ''
    
    await itemsApi.requestItem(selectedItem.value.id, requestData)
    
    closeRequestForm()
    await loadItems(pagination.value.current_page, searchQuery.value, filterType.value)
    
  } catch (err: any) {
    console.error('Error submitting request:', err)
    error.value = $t('errors.failed_to_submit_request')
  } finally {
    submittingRequest.value = false
  }
}

const goToPage = (page: number): void => {
  if (page >= 1 && page <= pagination.value.total_pages) {
    loadItems(page, searchQuery.value, filterType.value)
  }
}

const handleLogout = async (): Promise<void> => {
  if (isLoggingOut.value) return // Prevent multiple clicks
  
  try {
    isLoggingOut.value = true
    await logout()
  } catch (error: any) {
    console.error('Logout error:', error)
  } finally {
    isLoggingOut.value = false
  }
}

// Authentication check
onMounted(async () => {
  // Check authentication on client side
  if (process.client) {
    isAuthenticating.value = true
    try {
      const { authApi } = await import('~~/services/api')
      await authApi.validateCookies()

      // If successful, load data
      await loadItems()
    } catch (error) {
      // Redirect to login if not authenticated
      await navigateTo('/login')
    } finally {
      isAuthenticating.value = false
    }
  }
})
</script>

<style scoped>
.mobile-container {
  max-width: 375px;
  margin: 0 auto;
}
</style>

<style scoped>
/* Additional styles if needed */
</style>
