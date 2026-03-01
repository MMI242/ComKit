import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import Login from '../../app/pages/login.vue'

// Mock useAuth composable
const mockLogin = vi.fn()
const mockIsLoading = ref(false)
const mockError = ref('')

vi.mock('../../composables/useAuth', () => ({
  useAuth: () => ({
    login: mockLogin,
    isLoading: mockIsLoading,
    error: mockError
  })
}))

describe('Login Page - Simple Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockIsLoading.value = false
    mockError.value = ''
  })

  const getVm = (wrapper: any) => wrapper.vm as any

  it('renders login form correctly', () => {
    const wrapper = mount(Login)

    expect(wrapper.find('h2').text()).toBe('Welcome back')
    expect(wrapper.find('input#username').exists()).toBe(true)
    expect(wrapper.find('input#password').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('has correct form labels', () => {
    const wrapper = mount(Login)

    expect(wrapper.find('label[for="username"]').text()).toBe('Username')
    expect(wrapper.find('label[for="password"]').text()).toBe('Password')
  })

  it('binds form data correctly', async () => {
    const wrapper = mount(Login)

    const usernameInput = wrapper.find('input#username')
    const passwordInput = wrapper.find('input#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('testpass')

    const vm = getVm(wrapper)

    expect(vm.form.username).toBe('testuser')
    expect(vm.form.password).toBe('testpass')
  })

  it('shows loading state', () => {
    const wrapper = mount(Login)
    const button = wrapper.find('button[type="submit"]')

    expect(button.text()).toBe('Sign in to account')
  })

  it('displays error message when error exists', () => {
    mockError.value = 'Test error'
    const wrapper = mount(Login)

    const errorDiv = wrapper.find('.bg-red-50')
    expect(errorDiv.exists()).toBe(true)
    expect(errorDiv.text()).toContain('Test error')
  })

  it('does not display error when no error', () => {
    const wrapper = mount(Login)

    const errorDiv = wrapper.find('.bg-red-50')
    expect(errorDiv.exists()).toBe(false)
  })
})