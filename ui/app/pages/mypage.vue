<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold text-primary-700">ComKit</h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <NuxtLink
                to="/dashboard"
                class="border-transparent text-primary-600 hover:border-primary-300 hover:text-primary-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Homepage
              </NuxtLink>
              <NuxtLink
                to="/recipe"
                class="border-transparent text-primary-600 hover:border-primary-300 hover:text-primary-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Resep
              </NuxtLink>
              <NuxtLink
                to="/mypage"
                class="border-primary-400 text-primary-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium relative"
              >
                MyPage
                <span v-if="incomingRequestsCount > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                  {{ incomingRequestsCount }}
                </span>
              </NuxtLink>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="showAddItemModal = true"
              class="relative inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            >
              + Add Item
            </button>
            <button
              @click="handleLogout"
              :disabled="isLoggingOut"
              class="relative inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isLoggingOut" class="mr-2">
                <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              {{ isLoggingOut ? 'Logging out...' : 'Logout' }}
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Section Item Saya -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Item Saya</h2>
          <div class="bg-white shadow overflow-hidden sm:rounded-md">
            <div v-if="userItems.length === 0" class="text-center py-8">
              <p class="text-gray-500">Belum ada item yang dibagikan.</p>
              <button
                @click="showAddItemModal = true"
                class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Tambah Item Pertama
              </button>
            </div>
            <ul v-else role="list" class="divide-y divide-gray-200">
              <li v-for="item in userItems" :key="item.id" class="px-6 py-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <img
                      v-if="item.thumbnail_url"
                      :src="item.thumbnail_url"
                      :alt="item.name"
                      class="h-12 w-12 rounded-lg object-cover mr-4"
                    />
                    <div v-else class="h-12 w-12 rounded-lg bg-gray-200 flex items-center justify-center mr-4">
                      <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                      </svg>
                    </div>
                    <div>
                      <h3 class="text-lg font-medium text-gray-900">{{ item.name }}</h3>
                      <p class="text-sm text-gray-500">{{ item.description }}</p>
                      <p class="text-sm text-gray-500">
                        Qty: {{ item.remaining_qty }}/{{ item.qty }} {{ item.unit }} |
                        Type: {{ item.type === 'borrow' ? 'Pinjam' : 'Bagikan' }} |
                        Status: {{ item.status === 'available' ? 'Tersedia' : 'Dipinjam' }}
                      </p>
                    </div>
                  </div>
                  <div class="flex space-x-2">
                    <button
                      @click="editItem(item)"
                      class="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                      Edit
                    </button>
                    <button
                      @click="deleteItem(item.id)"
                      class="inline-flex items-center px-3 py-1 border border-red-300 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      Hapus
                    </button>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Section Request Masuk -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Request Masuk</h2>
          <div class="bg-white shadow overflow-hidden sm:rounded-md">
            <div v-if="incomingRequests.length === 0" class="text-center py-8">
              <p class="text-gray-500">Belum ada request masuk.</p>
            </div>
            <ul v-else role="list" class="divide-y divide-gray-200">
              <li v-for="request in incomingRequests" :key="request.id" class="px-6 py-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <img
                      v-if="request.item.thumbnail_url"
                      :src="request.item.thumbnail_url"
                      :alt="request.item.name"
                      class="h-12 w-12 rounded-lg object-cover mr-4"
                    />
                    <div v-else class="h-12 w-12 rounded-lg bg-gray-200 flex items-center justify-center mr-4">
                      <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                      </svg>
                    </div>
                    <div>
                      <h3 class="text-lg font-medium text-gray-900">{{ request.item.name }}</h3>
                      <p class="text-sm text-gray-500">Dari: {{ request.requester?.name }} ({{ request.requester?.username }})</p>
                      <p class="text-sm text-gray-500">
                        Qty: {{ request.requested_qty }} {{ request.unit }} |
                        Tanggal: {{ formatDate(request.date_start) }} - {{ formatDate(request.date_end) }} |
                        Status: <span :class="getStatusColor(request.status)">{{ getStatusText(request.status) }}</span>
                      </p>
                    </div>
                  </div>
                  <div class="flex space-x-2" v-if="request.status === 'pending'">
                    <button
                      @click="updateRequestStatus(request.id, 'approved')"
                      class="inline-flex items-center px-3 py-1 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                    >
                      Approve
                    </button>
                    <button
                      @click="updateRequestStatus(request.id, 'rejected')"
                      class="inline-flex items-center px-3 py-1 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      Reject
                    </button>
                  </div>
                  <div class="flex space-x-2" v-else-if="request.status === 'approved'">
                    <button
                      @click="updateRequestStatus(request.id, 'returned')"
                      class="inline-flex items-center px-3 py-1 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Sudah Dikembalikan
                    </button>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Section Request Saya -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Request Saya</h2>
          <div class="bg-white shadow overflow-hidden sm:rounded-md">
            <div v-if="outgoingRequests.length === 0" class="text-center py-8">
              <p class="text-gray-500">Belum ada request yang dikirim.</p>
            </div>
            <ul v-else role="list" class="divide-y divide-gray-200">
              <li v-for="request in outgoingRequests" :key="request.id" class="px-6 py-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <img
                      v-if="request.item.thumbnail_url"
                      :src="request.item.thumbnail_url"
                      :alt="request.item.name"
                      class="h-12 w-12 rounded-lg object-cover mr-4"
                    />
                    <div v-else class="h-12 w-12 rounded-lg bg-gray-200 flex items-center justify-center mr-4">
                      <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                      </svg>
                    </div>
                    <div>
                      <h3 class="text-lg font-medium text-gray-900">{{ request.item.name }}</h3>
                      <p class="text-sm text-gray-500">Kepada: {{ request.owner?.name }} ({{ request.owner?.username }})</p>
                      <p class="text-sm text-gray-500">
                        Qty: {{ request.requested_qty }} {{ request.unit }} |
                        Tanggal: {{ formatDate(request.date_start) }} - {{ formatDate(request.date_end) }} |
                        Status: <span :class="getStatusColor(request.status)">{{ getStatusText(request.status) }}</span>
                      </p>
                    </div>
                  </div>
                  <div class="flex space-x-2" v-if="request.status === 'pending'">
                    <button
                      @click="updateRequestStatus(request.id, 'cancelled')"
                      class="inline-flex items-center px-3 py-1 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>

    <!-- Add/Edit Item Modal -->
    <div v-if="showAddItemModal || editingItem" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click.self="closeItemModal">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingItem ? 'Edit Item' : 'Tambah Item Baru' }}
          </h3>
          <form @submit.prevent="submitItemForm" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Nama Item</label>
              <input
                v-model="itemForm.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Deskripsi</label>
              <textarea
                v-model="itemForm.description"
                rows="3"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              ></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Qty</label>
                <input
                  v-model.number="itemForm.qty"
                  type="number"
                  min="1"
                  required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Unit</label>
                <input
                  v-model="itemForm.unit"
                  type="text"
                  placeholder="pcs"
                  required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Tipe</label>
              <select
                v-model="itemForm.type"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="borrow">Pinjam</option>
                <option value="share">Bagikan</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Status</label>
              <select
                v-model="itemForm.status"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="available">Tersedia</option>
                <option value="borrowed">Dipinjam</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Foto Item</label>
              <input
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
                Batal
              </button>
              <button
                type="submit"
                :disabled="isSubmittingItem"
                class="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="isSubmittingItem" class="mr-2">
                  <svg class="animate-spin h-4 w-4 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ isSubmittingItem ? 'Menyimpan...' : 'Simpan' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click.self="showDeleteModal = false">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Konfirmasi Hapus</h3>
          <p class="text-sm text-gray-500 mb-4">
            Apakah Anda yakin ingin menghapus item "{{ itemToDelete?.name }}"?
            Tindakan ini tidak dapat dibatalkan.
          </p>
          <div class="flex justify-end space-x-3">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Batal
            </button>
            <button
              @click="confirmDeleteItem"
              :disabled="isDeletingItem"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isDeletingItem" class="mr-2">
                <svg class="animate-spin h-4 w-4 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              {{ isDeletingItem ? 'Menghapus...' : 'Hapus' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <AuthLoadingOverlay :is-authenticating="isAuthenticating" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { userItemsApi, userRequestsApi, UserItem, RequestResponse } from '~~/services/api'
import AuthLoadingOverlay from '~~/components/AuthLoadingOverlay.vue'

// Page metadata
definePageMeta({
  title: 'MyPage - ComKit',
  description: 'Manage your items and requests'
})

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
  isLoggingOut.value = true
  try {
    // Clear auth cookies
    await fetch('/auth/clear-cookies', { credentials: 'include' })
    // Redirect to login
    await navigateTo('/login')
  } catch (error) {
    console.error('Logout failed:', error)
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
  showAddItemModal.value = false
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
    alert('Nama item harus diisi')
    return
  }
  
  if (!itemForm.value.description.trim()) {
    alert('Deskripsi item harus diisi')
    return
  }
  
  if (!itemForm.value.qty || itemForm.value.qty <= 0) {
    alert('Quantity harus lebih besar dari 0')
    return
  }
  
  if (!itemForm.value.unit.trim()) {
    alert('Unit harus diisi')
    return
  }
  
  if (!['borrow', 'share'].includes(itemForm.value.type)) {
    alert('Tipe item harus dipilih')
    return
  }
  
  if (!['available', 'borrowed'].includes(itemForm.value.status)) {
    alert('Status item harus dipilih')
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
      const detail = error.detail || error.message || error.error || 'Data tidak valid'
      alert(`Gagal menyimpan item: ${detail}`)
    } else if (error.status === 401) {
      alert('Sesi login telah berakhir. Silakan login kembali.')
      await navigateTo('/login')
    } else if (error.status === 403) {
      alert('Anda tidak memiliki izin untuk melakukan tindakan ini.')
    } else {
      alert('Gagal menyimpan item. Silakan coba lagi.')
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
    alert('Gagal menghapus item. Silakan coba lagi.')
  } finally {
    isDeletingItem.value = false
  }
}

const updateRequestStatus = async (requestId: number, status: string) => {
  try {
    await userRequestsApi.updateRequestStatus(requestId, { status })
    await Promise.all([loadRequests(), loadUserItems()])
  } catch (error) {
    console.error('Failed to update request status:', error)
    alert('Gagal mengupdate status request. Silakan coba lagi.')
  }
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

const getStatusText = (status: string) => {
  switch (status) {
    case 'pending': return 'Pending'
    case 'approved': return 'Disetujui'
    case 'rejected': return 'Ditolak'
    case 'returned': return 'Dikembalikan'
    case 'cancelled': return 'Dibatalkan'
    default: return status
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
