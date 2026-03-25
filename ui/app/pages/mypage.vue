<template>
  <div class="min-h-screen bg-gray-50 mobile-container">
    <TopHeader :user="user" :is-logging-out="isLoggingOut" @logout="handleLogout" />

    <!-- Main content -->
    <main class="pt-12 pb-16 px-4">
      <!-- Section Item Saya -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-4 mt-5">
          <h2 class="text-2xl font-bold text-gray-900">{{ $t('mypage.my_items') }}</h2>
          <button @click="showAddItemModal = true" class="inline-flex items-center justify-center bg-primary-600 text-white py-1 px-2 rounded-lg hover:bg-primary-700 transition-colors duration-200 font-medium shadow-md text-sm">
            <Plus class="w-3 h-3 mr-1" />
            {{ $t('mypage.add_new_item') }}
          </button>
        </div>
        <div class="bg-white shadow overflow-hidden sm:rounded-md">
          <div v-if="userItems.length === 0" class="text-center py-8">
            <p class="text-gray-500">{{ $t('mypage.no_items_shared') }}</p>
          </div>
          <ul v-if="userItems.length > 0" role="list" class="divide-y divide-gray-200">
            <li v-for="item in userItems" :key="item.id" class="px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <img
                    :src="item.thumbnail_url || defaultImage"
                    @error="handleImageError"
                    :alt="item.name"
                    class="h-12 w-12 rounded-lg object-cover mr-4"
                  />
                  <div>
                    <h3 class="text-lg font-medium text-gray-900">{{ item.name }}</h3>
                    <p class="text-sm text-gray-500">{{ item.description }}</p>
                    <p class="text-sm text-gray-500">
                      {{ $t('mypage.qty') }}: {{ item.remaining_qty }}/{{ item.qty }} {{ item.unit }} |
                      {{ $t('mypage.type') }}: {{ item.type === 'borrow' ? $t('mypage.borrow') : $t('mypage.share') }} |
                      {{ $t('mypage.status') }}: {{ item.status === 'available' ? $t('mypage.available') : $t('mypage.borrowed') }}
                    </p>
                  </div>
                </div>
                <div class="flex space-x-2">
                  <button
                    @click="editItem(item)"
                    class="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    {{ $t('mypage.edit') }}
                  </button>
                  <button
                    @click="deleteItem(item.id)"
                    class="inline-flex items-center px-3 py-1 border border-red-300 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    {{ $t('mypage.delete') }}
                  </button>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Section Request Masuk -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">{{ $t('mypage.incoming_requests') }}</h2>
        <div class="bg-white shadow overflow-hidden sm:rounded-md">
          <div v-if="incomingRequests.length === 0" class="text-center py-8">
            <p class="text-gray-500">{{ $t('mypage.no_incoming_requests') }}</p>
          </div>
          <ul v-else role="list" class="divide-y divide-gray-200">
            <li v-for="request in incomingRequests" :key="request.id" class="px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <img
                    :src="request.item.thumbnail_url || defaultImage"
                    @error="handleImageError"
                    :alt="request.item.name"
                    class="h-12 w-12 rounded-lg object-cover mr-4"
                  />
                  <div>
                    <h3 class="text-lg font-medium text-gray-900">{{ request.item.name }}</h3>
                    <p class="text-sm text-gray-500">{{ $t('mypage.from') }}: {{ request.requester?.name }} ({{ request.requester?.username }})</p>
                    <p class="text-sm text-gray-500">
                      {{ $t('mypage.qty') }}: {{ request.requested_qty }} {{ request.unit }} |
                      {{ $t('mypage.date') }}: {{ formatDate(request.date_start) }} - {{ formatDate(request.date_end) }} |
                      {{ $t('mypage.status') }}: <span :class="getStatusColor(request.status)">{{ getStatusActionText(request.status) }}</span>
                    </p>
                  </div>
                </div>
                <div class="flex space-x-2" v-if="request.status === 'pending'">
                  <button
                    @click="openStatusModal(request, 'approved')"
                    class="inline-flex items-center px-3 py-1 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  >
                    {{ $t('mypage.approve') }}
                  </button>
                  <button
                    @click="openStatusModal(request, 'rejected')"
                    class="inline-flex items-center px-3 py-1 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    {{ $t('mypage.reject') }}
                  </button>
                </div>
                <div class="flex space-x-2" v-else-if="request.status === 'approved'">
                  <button
                    @click="openStatusModal(request, 'returned')"
                    class="inline-flex items-center px-3 py-1 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    {{ $t('mypage.returned') }}
                  </button>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Section Request Saya -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">{{ $t('mypage.my_requests') }}</h2>
        <div class="bg-white shadow overflow-hidden sm:rounded-md">
          <div v-if="outgoingRequests.length === 0" class="text-center py-8">
            <p class="text-gray-500">{{ $t('mypage.no_outgoing_requests') }}</p>
          </div>
          <ul v-else role="list" class="divide-y divide-gray-200">
            <li v-for="request in outgoingRequests" :key="request.id" class="px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <img
                    :src="request.item.thumbnail_url || defaultImage"
                    @error="handleImageError"
                    :alt="request.item.name"
                    class="h-12 w-12 rounded-lg object-cover mr-4"
                  />
                  <div>
                    <h3 class="text-lg font-medium text-gray-900">{{ request.item.name }}</h3>
                    <p class="text-sm text-gray-500">{{ $t('mypage.to') }}: {{ request.owner?.name }} ({{ request.owner?.username }})</p>
                    <p class="text-sm text-gray-500">
                      {{ $t('mypage.qty') }}: {{ request.requested_qty }} {{ request.unit }} |
                      {{ $t('mypage.date') }}: {{ formatDate(request.date_start) }} - {{ formatDate(request.date_end) }} |
                      {{ $t('mypage.status') }}: <span :class="getStatusColor(request.status)">{{ getStatusActionText(request.status) }}</span>
                    </p>
                  </div>
                </div>
                <div class="flex space-x-2" v-if="request.status === 'pending'">
                  <button
                    @click="openStatusModal(request, 'cancelled')"
                    class="inline-flex items-center px-3 py-1 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    {{ $t('mypage.cancel') }}
                  </button>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </main>

    <!-- Status Update Confirmation Modal -->
    <div v-if="showStatusModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click.self="cancelStatusUpdate">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-md mx-4 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">{{ $t('mypage.confirm_status_update') }}</h3>
          <p class="text-sm text-gray-500 mb-4">
            {{ $t('mypage.confirm_status_message', { action: getStatusActionText(newStatus!), requester: selectedRequest?.requester?.name, item: selectedRequest?.item.name }) }}
          </p>
          <div class="flex justify-end space-x-3">
            <button
              @click="cancelStatusUpdate"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              {{ $t('mypage.cancel') }}
            </button>
            <button
              @click="confirmStatusUpdate"
              class="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              {{ $t('common.confirm') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Item Modal -->
    <div v-if="showAddItemModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click.self="closeItemModal">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-md mx-4 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">{{ editingItem ? $t('mypage.edit_item') : $t('mypage.add_new_item_title') }}</h3>
          <form @submit.prevent="submitItemForm" class="space-y-4">
            <div>
              <label for="item-name" class="block text-sm font-medium text-gray-700">Nama Item</label>
              <input
                id="item-name"
                v-model="itemForm.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                placeholder="Masukkan nama item"
              />
            </div>
            <div>
              <label for="item-description" class="block text-sm font-medium text-gray-700">Deskripsi</label>
              <textarea
                id="item-description"
                v-model="itemForm.description"
                rows="3"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                placeholder="Masukkan deskripsi item"
              />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="item-qty" class="block text-sm font-medium text-gray-700">Quantity</label>
                <input
                  id="item-qty"
                  v-model.number="itemForm.qty"
                  type="number"
                  min="1"
                  required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              <div>
                <label for="item-unit" class="block text-sm font-medium text-gray-700">Unit</label>
                <input
                  id="item-unit"
                  v-model="itemForm.unit"
                  type="text"
                  required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                  placeholder="pcs, kg, etc."
                />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Tipe</label>
              <div class="mt-1">
                <label class="inline-flex items-center">
                  <input
                    v-model="itemForm.type"
                    type="radio"
                    value="borrow"
                    class="form-radio h-4 w-4 text-primary-600"
                  />
                  <span class="ml-2">Pinjam</span>
                </label>
                <label class="inline-flex items-center ml-6">
                  <input
                    v-model="itemForm.type"
                    type="radio"
                    value="share"
                    class="form-radio h-4 w-4 text-primary-600"
                  />
                  <span class="ml-2">Bagikan</span>
                </label>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Status</label>
              <div class="mt-1">
                <label class="inline-flex items-center">
                  <input
                    v-model="itemForm.status"
                    type="radio"
                    value="available"
                    class="form-radio h-4 w-4 text-primary-600"
                  />
                  <span class="ml-2">Tersedia</span>
                </label>
                <label class="inline-flex items-center ml-6">
                  <input
                    v-model="itemForm.status"
                    type="radio"
                    value="borrowed"
                    class="form-radio h-4 w-4 text-primary-600"
                  />
                  <span class="ml-2">Dipinjam</span>
                </label>
              </div>
            </div>
            <div>
              <label for="item-photo" class="block text-sm font-medium text-gray-700">Foto (Opsional)</label>
              <input
                id="item-photo"
                ref="photoInput"
                type="file"
                accept="image/*"
                @change="handlePhotoChange"
                class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
              />
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeItemModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                {{ $t('mypage.cancel') }}
              </button>
              <button
                type="submit"
                :disabled="isSubmittingItem"
                class="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {{ isSubmittingItem ? 'Menyimpan...' : (editingItem ? 'Update Item' : 'Tambah Item') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click.self="showDeleteModal = false">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-md mx-4 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Konfirmasi Hapus Item</h3>
          <p class="text-sm text-gray-500 mb-4">
            Apakah Anda yakin ingin menghapus item "<b>{{ itemToDelete?.name }}</b>"?
            Tindakan ini tidak dapat dibatalkan.
          </p>
          <div class="flex justify-end space-x-3">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              {{ $t('mypage.cancel') }}
            </button>
            <button
              @click="confirmDeleteItem"
              :disabled="isDeletingItem"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
            >
              {{ isDeletingItem ? 'Menghapus...' : 'Hapus' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Navigation -->
    <BottomNavigation :incomingRequestsCount="incomingRequestsCount" />

    <AuthLoadingOverlay :is-authenticating="isAuthenticating" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { userItemsApi, userRequestsApi, authApi } from '~~/services/api'
import type { UserItem, RequestResponse } from '~~/services/api'
import AuthLoadingOverlay from '~~/components/AuthLoadingOverlay.vue'
import { useAuth } from "~~/composables/useAuth"
import BottomNavigation from '~~/components/BottomNavigation.vue'
import TopHeader from '~~/components/TopHeader.vue'
import { Plus } from 'lucide-vue-next'

const runtimeConfig = useRuntimeConfig()
const defaultImage = runtimeConfig.public.defaultPlaceholderImage

type RequestStatusUpdateStatus = 'approved' | 'rejected' | 'returned' | 'cancelled'

// Page metadata
definePageMeta({
  title: 'MyPage - ComKit',
  description: 'Manage your items and requests'
})

// Use auth composable
const { user: authUser, logout } = useAuth()

// Computed user data from auth
const user = computed(() => authUser.value || { name: 'User', username: 'user' })

// Reactive data
const userItems = ref<UserItem[]>([])
const incomingRequests = ref<RequestResponse[]>([])
const outgoingRequests = ref<RequestResponse[]>([])
const isLoggingOut = ref(false)

const showAddItemModal = ref(false)
const editingItem = ref<UserItem | null>(null)
const showDeleteModal = ref(false)
const itemToDelete = ref<UserItem | null>(null)
const isSubmittingItem = ref(false)
const isDeletingItem = ref(false)
const isAuthenticating = ref(false)

const showStatusModal = ref(false)
const selectedRequest = ref<RequestResponse | null>(null)
const newStatus = ref<RequestStatusUpdateStatus | null>(null)

const itemForm = ref({
  name: '',
  description: '',
  qty: 1,
  unit: 'pcs',
  type: 'borrow' as 'borrow' | 'share',
  status: 'available' as 'available' | 'borrowed',
  photo: null as File | null
})

const photoInput = ref<HTMLInputElement | null>(null)

// Computed
const incomingRequestsCount = computed(() => {
  return incomingRequests.value.filter(req => req.status === 'pending').length
})

// Methods
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = defaultImage
}
const loadUserItems = async () => {
  try {
    const response = await userItemsApi.getUserItems()
    userItems.value = response.items
  } catch (error) {
    console.error('Failed to load user items:', error)
  }
}

const loadRequests = async () => {
  try {
    const [incoming, outgoing] = await Promise.all([
      userRequestsApi.getUserRequests('incoming'),
      userRequestsApi.getUserRequests('outgoing')
    ])
    incomingRequests.value = incoming.requests
    outgoingRequests.value = outgoing.requests
  } catch (error) {
    console.error('Failed to load requests:', error)
  }
}

const handleLogout = async () => {
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

const editItem = (item: UserItem) => {
  editingItem.value = item
  itemForm.value = {
    name: item.name,
    description: item.description,
    qty: item.qty,
    unit: item.unit,
    type: item.type,
    status: item.status,
    photo: null
  }
  showAddItemModal.value = true
}

const closeItemModal = () => {
  showAddItemModal.value = false
  editingItem.value = null
  itemForm.value = {
    name: '',
    description: '',
    qty: 1,
    unit: 'pcs',
    type: 'borrow',
    status: 'available',
    photo: null
  }
  if (photoInput.value) {
    photoInput.value.value = ''
  }
}

const handlePhotoChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    itemForm.value.photo = target.files[0]
  }
}

const submitItemForm = async () => {
  // Frontend validation before API call
  if (!itemForm.value.name.trim()) {
    alert($t('mypage.item_name_required'))
    return
  }
  
  if (!itemForm.value.description.trim()) {
    alert($t('mypage.description_required'))
    return
  }
  
  if (!itemForm.value.qty || itemForm.value.qty <= 0) {
    alert($t('mypage.quantity_greater_zero'))
    return
  }
  
  if (!itemForm.value.unit.trim()) {
    alert($t('mypage.unit_required'))
    return
  }
  
  if (!['borrow', 'share'].includes(itemForm.value.type)) {
    alert($t('mypage.type_required'))
    return
  }
  
  if (!['available', 'borrowed'].includes(itemForm.value.status)) {
    alert($t('mypage.status_required'))
    return
  }

  isSubmittingItem.value = true
  try {
    const formData = new FormData()
    formData.append('name', itemForm.value.name.trim())
    formData.append('description', itemForm.value.description.trim())
    formData.append('qty', itemForm.value.qty.toString())
    formData.append('unit', itemForm.value.unit.trim())
    formData.append('type', itemForm.value.type)
    formData.append('status', itemForm.value.status)
    if (itemForm.value.photo) {
      formData.append('photo', itemForm.value.photo)
    }

    if (editingItem.value) {
      await userItemsApi.updateUserItem(editingItem.value.id, formData)
    } else {
      await userItemsApi.createUserItem(formData)
    }

    await loadUserItems()
    closeItemModal()
  } catch (error: any) {
    console.error('Failed to save item:', error)
    
    // Show more specific error messages
    if (error.status === 400) {
      // Try to extract the detail message from different possible formats
      const detail = error.detail || error.message || error.error || $t('mypage.invalid_data')
      alert($t('mypage.failed_to_save_item', { error: detail }))
    } else if (error.status === 401) {
      alert($t('mypage.session_expired'))
      await navigateTo('/login')
    } else if (error.status === 403) {
      alert($t('mypage.no_permission'))
    } else {
      alert($t('mypage.failed_to_save'))
    }
  } finally {
    isSubmittingItem.value = false
  }
}

const deleteItem = (itemId: number) => {
  const item = userItems.value.find(i => i.id === itemId)
  if (item) {
    itemToDelete.value = item
    showDeleteModal.value = true
  }
}

const confirmDeleteItem = async () => {
  if (!itemToDelete.value) return

  isDeletingItem.value = true
  try {
    await userItemsApi.deleteUserItem(itemToDelete.value.id)
    await loadUserItems()
    showDeleteModal.value = false
    itemToDelete.value = null
  } catch (error) {
    console.error('Failed to delete item:', error)
    alert($t('mypage.failed_to_delete'))
  } finally {
    isDeletingItem.value = false
  }
}

const openStatusModal = (request: RequestResponse, status: RequestStatusUpdateStatus) => {
  selectedRequest.value = request
  newStatus.value = status
  showStatusModal.value = true
}

const updateRequestStatus = async (requestId: number, status: RequestStatusUpdateStatus) => {
  try {
    await userRequestsApi.updateRequestStatus(requestId, { status })
    await Promise.all([loadRequests(), loadUserItems()])
  } catch (error) {
    console.error('Failed to update request status:', error)
    alert($t('mypage.failed_to_update_status'))
  }
}

const confirmStatusUpdate = async () => {
  if (!selectedRequest.value || !newStatus.value) return

  await updateRequestStatus(selectedRequest.value.id, newStatus.value as RequestStatusUpdateStatus)
  showStatusModal.value = false
  selectedRequest.value = null
  newStatus.value = null
}

const cancelStatusUpdate = () => {
  showStatusModal.value = false
  selectedRequest.value = null
  newStatus.value = null
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('id-ID')
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending': return 'text-yellow-600'
    case 'approved': return 'text-green-600'
    case 'rejected': return 'text-red-600'
    case 'returned': return 'text-blue-600'
    case 'cancelled': return 'text-gray-600'
    default: return 'text-gray-600'
  }
}

const getStatusActionText = (status: string) => {
  switch (status) {
    case 'approved': return $t('mypage.approve_action')
    case 'rejected': return $t('mypage.reject_action')
    case 'returned': return $t('mypage.return_action')
    case 'cancelled': return $t('mypage.cancel_action')
    default: return 'mengupdate'
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
      // Small delay to ensure cookies are set
      await new Promise(resolve => setTimeout(resolve, 100))
      // If successful, load data
      await Promise.all([loadUserItems(), loadRequests()])
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
