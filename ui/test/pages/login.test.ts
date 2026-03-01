import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import Login from '../../app/pages/login.vue'

// Mock navigateTo globally
const mockNavigateTo = vi.fn()
globalThis.navigateTo = mockNavigateTo

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

describe('Login Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockIsLoading.value = false
    mockError.value = ''
  })

  const getVm = (wrapper: any) => wrapper.vm as any

  it('renders login form correctly', () => {
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

    expect(wrapper.find('h2').text()).toBe('Welcome back')
    expect(wrapper.find('input#username').exists()).toBe(true)
    expect(wrapper.find('input#password').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
    expect(wrapper.find('input[type="checkbox"]').exists()).toBe(true)
  })

  it('has correct form labels and placeholders', () => {
    const wrapper = mount(Login)

    // Menyesuaikan dengan placeholder di layout baru
    expect(wrapper.find('input#username').attributes('placeholder')).toBe('Enter username')
    expect(wrapper.find('input#password').attributes('placeholder')).toBe('••••••••')
  })

  it('binds form data correctly', async () => {
    const wrapper = mount(Login)
    const vm = getVm(wrapper)

    await wrapper.find('input#username').setValue('testuser')
    await wrapper.find('input#password').setValue('testpass')

    expect(vm.form.username).toBe('testuser')
    expect(vm.form.password).toBe('testpass')
  })

  it('toggles remember me checkbox', async () => {
    const wrapper = mount(Login)
    const vm = getVm(wrapper)

    expect(vm.form.rememberMe).toBe(false)

    await (wrapper.find('input[type="checkbox"]') as any).setChecked(true)
    expect(vm.form.rememberMe).toBe(true)
  })

  it('shows loading state', () => {
    const wrapper = mount(Login)

    expect(wrapper.find('button[type="submit"]').text()).toBe('Sign in to account')
  })

  it('displays error message when error exists', () => {
    mockError.value = 'Test error'
    const wrapper = mount(Login)

    expect(wrapper.find('.bg-red-50').exists()).toBe(true)
    expect(wrapper.find('.bg-red-50').text()).toContain('Test error')
  })

  it('submits form with correct data', async () => {
    const wrapper = mount(Login)
    const vm = getVm(wrapper)

    await wrapper.find('input#username').setValue('test')
    await wrapper.find('input#password').setValue('password')
    await wrapper.find('form').trigger('submit.prevent')

    expect(vm.form.username).toBe('test')
    expect(vm.form.password).toBe('password')
  })

  it('calls login function with correct credentials', async () => {
    mockLogin.mockResolvedValue(undefined)
    mockNavigateTo.mockResolvedValue(undefined)

    const wrapper = mount(Login)

    await wrapper.find('input#username').setValue('test')
    await wrapper.find('input#password').setValue('password')
    await wrapper.find('form').trigger('submit.prevent')
    
    // Wait for async operations to complete
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 10))

    expect(mockLogin).toHaveBeenCalledWith('test', 'password', false)
    expect(mockNavigateTo).toHaveBeenCalledWith('/dashboard')
  })

  it('calls login with remember me when checked', async () => {
    mockLogin.mockResolvedValue(undefined)
    mockNavigateTo.mockResolvedValue(undefined)

    const wrapper = mount(Login)

    await wrapper.find('input#username').setValue('test')
    await wrapper.find('input#password').setValue('password')
    await (wrapper.find('input[type="checkbox"]') as any).setChecked(true)
    await wrapper.find('form').trigger('submit.prevent')
    
    // Wait for async operations to complete
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(mockLogin).toHaveBeenCalledWith('test', 'password', true)
    expect(mockNavigateTo).toHaveBeenCalledWith('/dashboard')
  })

  it('handles login error', async () => {
    const mockError = new Error('Invalid credentials')
    mockLogin.mockRejectedValue(mockError)

    const wrapper = mount(Login)

    await wrapper.find('input#username').setValue('wrong')
    await wrapper.find('input#password').setValue('wrong')
    await wrapper.find('form').trigger('submit.prevent')

    // Should not navigate on error
    expect(mockNavigateTo).not.toHaveBeenCalled()
  })
})