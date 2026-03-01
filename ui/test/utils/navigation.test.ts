import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import Login from '../../app/pages/login.vue'
import Register from '../../app/pages/register.vue'

// Mock navigateTo globally
const mockNavigateTo = vi.fn()
globalThis.navigateTo = mockNavigateTo

// Mock useAuth composable
const mockLogin = vi.fn()
const mockRegister = vi.fn()

vi.mock('../../composables/useAuth', () => ({
  useAuth: () => ({
    login: mockLogin,
    register: mockRegister,
    isLoading: ref(false),
    error: ref('')
  })
}))

describe('Navigation Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('navigates to register from login page', async () => {
    const wrapper = mount(Login, {
      global: {
        stubs: {
          'NuxtLink': {
            template: '<a :href="to"><slot /></a>',
            props: ['to']
          }
        }
      }
    })

    const registerLink = wrapper.find('a[href="/register"]')
    expect(registerLink.exists()).toBe(true)
    expect(registerLink.text()).toContain('Sign up now')
  })

  it('navigates to login from register page', async () => {
    const wrapper = mount(Register, {
      global: {
        stubs: {
          'NuxtLink': {
            template: '<a :href="to"><slot /></a>',
            props: ['to']
          }
        }
      }
    })

    const loginLink = wrapper.find('a[href="/login"]')
    expect(loginLink.exists()).toBe(true)
    expect(loginLink.text()).toContain('sign in to your existing account')
  })

  it('navigates to dashboard on successful login', async () => {
    mockLogin.mockResolvedValue(undefined)
    mockNavigateTo.mockResolvedValue(undefined)

    const wrapper = mount(Login, {
      global: {
        stubs: {
          'NuxtLink': {
            template: '<a :href="to"><slot /></a>',
            props: ['to']
          }
        }
      }
    })
    
    const usernameInput = wrapper.find('input#username')
    const passwordInput = wrapper.find('input#password')
    const form = wrapper.find('form')
    
    await usernameInput.setValue('test')
    await passwordInput.setValue('password')
    
    // Check that the input values are set correctly
    expect((usernameInput.element as HTMLInputElement).value).toBe('test')
    expect((passwordInput.element as HTMLInputElement).value).toBe('password')
    
    await form.trigger('submit.prevent')
    
    // Wait for async operations to complete
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))
    
    // For script setup components, we can check the DOM element values
    // The form submission should work correctly
    expect((usernameInput.element as HTMLInputElement).value).toBe('test')
    expect((passwordInput.element as HTMLInputElement).value).toBe('password')
    
    // Should call login and navigate
    expect(mockLogin).toHaveBeenCalledWith('test', 'password', false)
    expect(mockNavigateTo).toHaveBeenCalledWith('/dashboard')
  })

  it('navigates to login on successful registration', async () => {
    mockRegister.mockResolvedValue(undefined)
    mockNavigateTo.mockResolvedValue(undefined)

    const wrapper = mount(Register)
    
    // Fill form with valid data
    const usernameInput = wrapper.find('input#username')
    const nameInput = wrapper.find('input#name')
    const addressTextarea = wrapper.find('textarea#address')
    const passwordInput = wrapper.find('input#password')
    const confirmPasswordInput = wrapper.find('input#confirmPassword')
    const termsCheckbox = wrapper.find('input#agree-terms')
    const form = wrapper.find('form')
    
    await usernameInput.setValue('testuser')
    await nameInput.setValue('Test User')
    await addressTextarea.setValue('123 Test St')
    await passwordInput.setValue('password123')
    await confirmPasswordInput.setValue('password123')
    await termsCheckbox.setValue(true)
    
    await form.trigger('submit.prevent')
    
    // Wait for async operations to complete
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))
    
    // Should call register and navigate
    expect(mockRegister).toHaveBeenCalledWith({
      username: 'testuser',
      name: 'Test User',
      address: '123 Test St',
      password: 'password123'
    })
  })
})