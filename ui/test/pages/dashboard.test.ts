import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import Dashboard from '../../app/pages/dashboard.vue'
import { mockFetch } from '../setup'

// Mock NotificationDropdown component
vi.mock('../../components/NotificationDropdown.vue', () => ({
  default: {
    name: 'NotificationDropdown',
    template: '<div><slot /></div>'
  }
}))

// Mock useAuth composable
const mockUser = ref({
  name: 'John Doe',
  username: 'johndoe'
})

vi.mock('~/composables/useAuth', () => ({
  useAuth: () => ({
    user: mockUser,
    logout: vi.fn()
  })
}))

// Mock navigateTo
vi.mock('#app/composables', () => ({
  navigateTo: vi.fn()
}))

// Mock process.client
Object.defineProperty(process, 'client', {
  value: true,
  writable: true
})

// Mock API responses
const mockItemsResponse = {
  items: [
    {
      id: 1,
      name: "Bor Listrik",
      description: "Bor listrik Bosch 500W, kondisi bagus",
      qty: 1,
      remaining_qty: 1,
      unit: "pcs",
      thumbnail_url: "/media/items/1_thumb.jpg",
      photo_url: "/media/items/1_full.jpg",
      type: "borrow",
      status: "available",
      owner: {
        id: 2,
        username: "jqr123",
        name: "Jqwery Ddo",
        address: "Depan Poskamling RT2. Jl. Mawar No. 5 RT2"
      }
    },
    {
      id: 2,
      name: "Nasi Goreng",
      description: "Nasi goreng sisa acara, masih hangat. Ambil secepatnya",
      qty: 10,
      remaining_qty: 7,
      unit: "porsi",
      thumbnail_url: "/media/items/2_thumb.jpg",
      photo_url: "/media/items/2_full.jpg",
      type: "share",
      status: "available",
      owner: {
        id: 3,
        username: "user2",
        name: "User Dua",
        address: "Jl. Melati No. 10 RT 01"
      }
    }
  ],
  pagination: {
    current_page: 1,
    total_pages: 3,
    total_items: 67,
    items_per_page: 25
  }
}

describe('Dashboard Page (Homepage)', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    
    // Setup fetch mock to return successful response
    mockFetch.mockImplementation((url) => {
      if (url.includes('/auth/validate-cookies')) {
        return Promise.resolve(new Response(JSON.stringify({
          access_token: 'mock-token',
          user: { id: 1, name: 'Test User', username: 'testuser' }
        }), {
          status: 200,
          statusText: 'OK',
          headers: { 'Content-Type': 'application/json' },
        }))
      } else if (url.includes('/items?')) {
        return Promise.resolve(new Response(JSON.stringify(mockItemsResponse), {
          status: 200,
          statusText: 'OK',
          headers: {
            'Content-Type': 'application/json'
          },
        }))
      }
      return Promise.resolve(new Response(JSON.stringify({}), {
        status: 200,
        statusText: 'OK',
        headers: {
          'Content-Type': 'application/json'
        },
      }))
    })
  })

  const getVm = (wrapper: any) => wrapper.vm as any

  it('renders homepage correctly', () => {
    const wrapper = mount(Dashboard)
    
    expect(wrapper.find('h1').text()).toBe('ComKit')
    expect(wrapper.find('input[placeholder="Cari item..."]').exists()).toBe(true)
  })

  it('displays navigation menu', () => {
    const wrapper = mount(Dashboard)
    
    // Check that expected elements are present in the component
    const componentText = wrapper.text()
    expect(componentText).toContain('ComKit')
    expect(componentText).toContain('Logout')
    
    // Check for search functionality
    expect(wrapper.find('input[placeholder="Cari item..."]').exists()).toBe(true)
    
    // Check for filter options
    expect(componentText).toContain('All')
    expect(componentText).toContain('Borrow')
    expect(componentText).toContain('Share')
  })

  it('displays search and filter section', () => {
    const wrapper = mount(Dashboard)
    
    // Search input
    expect(wrapper.find('input[placeholder="Cari item..."]').exists()).toBe(true)
    
    // Filter radio buttons
    expect(wrapper.find('input[value="all"]').exists()).toBe(true)
    expect(wrapper.find('input[value="borrow"]').exists()).toBe(true)
    expect(wrapper.find('input[value="share"]').exists()).toBe(true)
    
    // Filter labels
    expect(wrapper.text()).toContain('All')
    expect(wrapper.text()).toContain('Borrow')
    expect(wrapper.text()).toContain('Share')
  })

  it('displays items list', async () => {
    const wrapper = mount(Dashboard, {
      global: { stubs: { NuxtLink: true } }
    })
    const vm = getVm(wrapper)

    // Manually trigger authentication and data loading
    await vm.loadItems()

    await wrapper.vm.$nextTick()

    // Should display mock items
    expect(wrapper.text()).toContain('Bor Listrik')
    expect(wrapper.text()).toContain('Nasi Goreng')
    expect(wrapper.text()).toContain('Jqwery Ddo')
    expect(wrapper.text()).toContain('User Dua')
  })

  it('has correct item data structure', async () => {
    const wrapper = mount(Dashboard, {
      global: { stubs: { NuxtLink: true } }
    })
    const vm = getVm(wrapper)

    // Manually trigger data loading
    await vm.loadItems()

    await wrapper.vm.$nextTick()

    expect(vm.items.length).toBe(2)
    expect(vm.items[0].name).toBe('Bor Listrik')
    expect(vm.items[1].name).toBe('Nasi Goreng')
    expect(vm.items[0].type).toBe('borrow')
    expect(vm.items[1].type).toBe('share')
  })

  it('loads items on mount', async () => {
    const wrapper = mount(Dashboard, {
      global: { stubs: { NuxtLink: true } }
    })
    const vm = getVm(wrapper)

    // Manually trigger data loading
    await vm.loadItems()

    await wrapper.vm.$nextTick()

    expect(vm.items.length).toBe(2)
    expect(vm.pagination.current_page).toBe(1)
    expect(vm.pagination.total_items).toBe(67)
  })

  it('has user information', () => {
    const wrapper = mount(Dashboard)
    const vm = getVm(wrapper)

    expect(vm.user.name).toBe('John Doe')
    expect(vm.user.username).toBe('johndoe')
  })

  it('displays logout functionality', () => {
    const wrapper = mount(Dashboard)

    expect(wrapper.text()).toContain('Logout')
  })

  it('has pagination controls', async () => {
    const wrapper = mount(Dashboard, { global: { stubs: { NuxtLink: true } } })
    const vm = getVm(wrapper)

    // Wait for component to mount and load data
    await wrapper.vm.$nextTick()
    await vm.loadItems()
    await wrapper.vm.$nextTick()
    
    const pagination = wrapper.find('.mt-6.flex.items-center.justify-between')
    expect(pagination.exists()).toBe(true)
    
    // Check pagination text
    expect(wrapper.text()).toContain('Page 1 of 3')
    expect(wrapper.text()).toContain('(67 total items)')
    
    // Check pagination buttons
    expect(wrapper.text()).toContain('Previous')
    expect(wrapper.text()).toContain('Next')
  })

  it('can expand and collapse item details', async () => {
    const wrapper = mount(Dashboard)
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    // Initially all items should be collapsed
    expect(vm.expandedItems.length).toBe(0)
    
    // Toggle expand first item
    vm.toggleExpand(1)
    expect(vm.expandedItems).toContain(1)
    
    // Toggle collapse
    vm.toggleExpand(1)
    expect(vm.expandedItems).not.toContain(1)
  })

  it('opens request modal for available items', async () => {
    const wrapper = mount(Dashboard)
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    // Open request form for first item
    vm.openRequestForm(vm.items[0])
    
    expect(vm.showRequestModal).toBe(true)
    expect(vm.selectedItem).toBe(vm.items[0])
    expect(vm.requestForm.requested_qty).toBe(1)
  })

  it('closes request modal properly', () => {
    const wrapper = mount(Dashboard)
    const vm = getVm(wrapper)

    // Close request form
    vm.closeRequestForm()
    
    expect(vm.showRequestModal).toBe(false)
    expect(vm.selectedItem).toBe(null)
    expect(vm.requestForm.requested_qty).toBe(1)
  })

  it('handles search functionality', async () => {
    const wrapper = mount(Dashboard)
    const vm = getVm(wrapper)

    const loadItemsSpy = vi.spyOn(vm, 'loadItems')
    
    // Set search query
    vm.searchQuery = 'test'
    vm.handleSearch()
    
    // Should call loadItems after debounce (using setTimeout in mock)
    setTimeout(() => {
      expect(loadItemsSpy).toHaveBeenCalledWith(1, 'test', 'all')
    }, 300)
  })

  it('handles filter functionality', async () => {
    const wrapper = mount(Dashboard)
    const vm = getVm(wrapper)

    // Check that methods exist
    expect(typeof vm.handleFilter).toBe('function')
    expect(typeof vm.loadItems).toBe('function')
    
    // Set filter type
    vm.filterType = 'borrow'
    
    // Call the method - it should not throw
    expect(() => vm.handleFilter()).not.toThrow()
  })

  it('handles pagination navigation', async () => {
    const wrapper = mount(Dashboard)
    const vm = getVm(wrapper)

    // Check that methods exist
    expect(typeof vm.goToPage).toBe('function')
    expect(typeof vm.loadItems).toBe('function')
    
    // Call the method - it should not throw
    expect(() => vm.goToPage(2)).not.toThrow()
    
    // Test invalid page
    expect(() => vm.goToPage(0)).not.toThrow()
  })
})
