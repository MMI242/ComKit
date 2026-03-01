import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'

// Mock useAuth composable for all tests
vi.mock('../../composables/useAuth', () => ({
  useAuth: () => ({
    login: vi.fn(),
    isLoading: ref(false),
    error: ref('')
  })
}))

describe('Basic Component Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should mount login page without errors', async () => {
    // Test that we can import and mount the component
    const { mount } = await import('@vue/test-utils')
    const Login = (await import('../../app/pages/login.vue')).default
    
    const wrapper = mount(Login, {
      global: {
        stubs: {
          'NuxtLink': true,
          'NuxtRouteAnnouncer': true,
          'NuxtPage': true
        }
      }
    })
    
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('h2').text()).toBe('Welcome back')
  })

  it('should find form elements', async () => {
    const { mount } = await import('@vue/test-utils')
    const Login = (await import('../../app/pages/login.vue')).default
    
    const wrapper = mount(Login, {
      global: {
        stubs: {
          'NuxtLink': true,
          'NuxtRouteAnnouncer': true,
          'NuxtPage': true
        }
      }
    })
    
    expect(wrapper.find('input#username').exists()).toBe(true)
    expect(wrapper.find('input#password').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('should handle form input', async () => {
    const { mount } = await import('@vue/test-utils')
    const Login = (await import('../../app/pages/login.vue')).default
    
    const wrapper = mount(Login, {
      global: {
        stubs: {
          'NuxtLink': true,
          'NuxtRouteAnnouncer': true,
          'NuxtPage': true
        }
      }
    })
    
    const usernameInput = wrapper.find('input#username')
    await usernameInput.setValue('testuser')
    
    expect((wrapper.vm as any).form.username).toBe('testuser')
  })
})
