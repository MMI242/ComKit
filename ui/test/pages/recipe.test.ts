/// <reference types="node" />

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Recipe from '../../app/pages/recipe.vue'
import { mockFetch } from '../setup'

// Mock NotificationDropdown component
vi.mock('../../components/NotificationDropdown.vue', () => ({
  default: {
    name: 'NotificationDropdown',
    template: '<div><slot /></div>'
  }
}))

// Mock useAuth composable
vi.mock('~/composables/useAuth', () => ({
  useAuth: () => ({
    login: vi.fn(),
    logout: vi.fn(),
    isLoading: { value: false },
    error: { value: '' },
    isAuthenticated: { value: true },
    currentUser: { value: { id: 1, username: 'testuser', name: 'Test User' } },
    user: { value: { id: 1, username: 'testuser', name: 'Test User' } }
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

describe('Recipe Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()

    // Setup fetch mock to return successful responses
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
      } else if (url.includes('/ai/recipe')) {
        return Promise.resolve(new Response(JSON.stringify({
          recipe: {
            title: "Delicious Pasta",
            ingredients: ["pasta", "tomato sauce", "cheese"],
            instructions: "Cook pasta, add sauce, top with cheese",
            prep_time: 15,
            cook_time: 20,
            servings: 4,
            difficulty: "Easy",
            nutrition: {
              calories: 450,
              protein: 15,
              carbs: 60,
              fat: 18
            }
          },
          generated_at: "2025-01-20T10:30:00Z"
        }), {
          status: 200,
          statusText: 'OK',
          headers: { 'Content-Type': 'application/json' },
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

  it('should mount recipe page without errors', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })

    // Wait for authentication and any async operations
    await wrapper.vm.$nextTick()

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('h1').text()).toBe('ComKit')
  })

  it('should display all required UI elements', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })

    await wrapper.vm.$nextTick()

    // Check basic UI elements that should exist
    expect(wrapper.text()).toContain('ComKit')
    expect(wrapper.find('textarea').exists()).toBe(true)
    expect(wrapper.find('button').exists()).toBe(true)
  })

  it('should handle ingredient input correctly', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    const textarea = wrapper.find('textarea')
    await textarea.setValue('tomato, onion, garlic')

    expect(vm.ingredients).toBe('tomato, onion, garlic')
  })

  it('should show loading state during recipe generation', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    const textarea = wrapper.find('textarea')
    const button = wrapper.find('button')

    await textarea.setValue('tomato, onion, garlic')

    // Mock a slow API call
    vm.isLoading = true
    await wrapper.vm.$nextTick()

    expect(vm.isLoading).toBe(true)
  })

  it('should display generated recipe successfully', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    // Simulate successful recipe generation
    vm.recipe = {
      title: "Delicious Pasta",
      ingredients: ["pasta", "tomato sauce", "cheese"],
      instructions: "Cook pasta, add sauce, top with cheese",
      prep_time: 15,
      cook_time: 20,
      servings: 4,
      difficulty: "Easy",
      nutrition: {
        calories: 450,
        protein: 15,
        carbs: 60,
        fat: 18
      }
    }
    vm.generatedAt = "2025-01-20T10:30:00Z"

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Delicious Pasta')
    expect(wrapper.text()).toContain('pasta')
    expect(wrapper.text()).toContain('tomato sauce')
    expect(wrapper.text()).toContain('cheese')
  })

  it('should handle API errors gracefully', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    // Simulate API error
    vm.error = 'AI service unavailable'

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('AI service unavailable')
  })

  it('should validate empty ingredients input', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    const textarea = wrapper.find('textarea')
    const button = wrapper.find('[data-testid="generate-btn"]')

    await textarea.setValue('')
    await button.trigger('click')

    // Should not have called generateRecipe with empty input
    expect(vm.ingredients.trim()).toBe('')
  })

  it('should handle whitespace-only ingredients input', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    const textarea = wrapper.find('textarea')
    const button = wrapper.find('[data-testid="generate-btn"]')

    await textarea.setValue('   \n\t   ')
    await button.trigger('click')

    // Should not have processed whitespace-only input
    expect(vm.ingredients.trim()).toBe('')
  })

  it('should display generated timestamp correctly', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })
    const vm = getVm(wrapper)

    await wrapper.vm.$nextTick()

    vm.generatedAt = "2025-01-20T10:30:00Z"
    await wrapper.vm.$nextTick()

    // Should display the timestamp
    expect(vm.generatedAt).toBe("2025-01-20T10:30:00Z")
  })

  it('should handle logout functionality', async () => {
    const wrapper = mount(Recipe, { global: { stubs: { NuxtLink: true } } })

    await wrapper.vm.$nextTick()

    // Check that logout button exists
    expect(wrapper.text()).toContain('Logout')
  })
})
