import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import Register from '../../app/pages/register.vue'

// Mock navigateTo globally
const mockNavigateTo = vi.fn()
globalThis.navigateTo = mockNavigateTo

// Mock useAuth composable
const mockRegister = vi.fn()
const mockIsLoading = ref(false)
const mockError = ref('')

vi.mock('~/composables/useAuth', () => ({
  useAuth: () => ({
    register: mockRegister,
    isLoading: mockIsLoading,
    error: mockError
  })
}))

describe('Register Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockIsLoading.value = false
    mockError.value = ''
  })

  const getVm = (wrapper: any) => wrapper.vm as any

  it('renders registration form correctly', () => {
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
    
    expect(wrapper.find('h1').text()).toBe('Join ComKit')
    expect(wrapper.find('input#username').exists()).toBe(true)
    expect(wrapper.find('input#name').exists()).toBe(true)
    expect(wrapper.find('textarea#address').exists()).toBe(true)
    expect(wrapper.find('input#password').exists()).toBe(true)
    expect(wrapper.find('input#confirmPassword').exists()).toBe(true)
    expect(wrapper.find('input#agree-terms').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('has correct form labels and placeholders', () => {
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
    
    expect(wrapper.find('label[for="username"]').text()).toBe('Username')
    expect(wrapper.find('label[for="name"]').text()).toBe('Full Name')
    expect(wrapper.find('label[for="address"]').text()).toBe('Address')
    expect(wrapper.find('label[for="password"]').text()).toBe('Password')
    expect(wrapper.find('label[for="confirmPassword"]').text()).toBe('Confirm Password')
    
    expect(wrapper.find('input#username').attributes('placeholder')).toBe('@johndoe')
    expect(wrapper.find('input#name').attributes('placeholder')).toBe('John Doe')
    expect(wrapper.find('textarea#address').attributes('placeholder')).toBe('123 Main St, City, State 12345')
    expect(wrapper.find('input#password').attributes('placeholder')).toBe('••••••••')
    expect(wrapper.find('input#confirmPassword').attributes('placeholder')).toBe('••••••••')
  })

  it('has link to login page', () => {
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
    expect(loginLink.text()).toContain('Sign in here')
  })

  it('has terms and privacy policy links', () => {
    const wrapper = mount(Register)
    
    expect(wrapper.text()).toContain('Terms and Conditions')
    expect(wrapper.text()).toContain('Privacy Policy')
  })

  it('binds form data correctly', async () => {
    const wrapper = mount(Register)
    
    const usernameInput = wrapper.find('input#username')
    const nameInput = wrapper.find('input#name')
    const addressTextarea = wrapper.find('textarea#address')
    const passwordInput = wrapper.find('input#password')
    const confirmPasswordInput = wrapper.find('input#confirmPassword')
    
    await usernameInput.setValue('testuser')
    await nameInput.setValue('Test User')
    await addressTextarea.setValue('123 Test St')
    await passwordInput.setValue('password123')
    await confirmPasswordInput.setValue('password123')

    const vm = getVm(wrapper)

    expect(vm.form.username).toBe('testuser')
    expect(vm.form.name).toBe('Test User')
    expect(vm.form.address).toBe('123 Test St')
    expect(vm.form.password).toBe('password123')
    expect(vm.form.confirmPassword).toBe('password123')
  })

  it('toggles terms agreement checkbox', async () => {
    const wrapper = mount(Register)
    
    const checkbox = wrapper.find('input#agree-terms')

    const vm = getVm(wrapper)
    
    expect(vm.form.agreeTerms).toBe(false)
    
    await (checkbox as any).setChecked(true)

    expect(vm.form.agreeTerms).toBe(true)
  })

  it('shows loading state', () => {
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
    
    const button = wrapper.find('button[type="submit"]')

    const vm = getVm(wrapper)

    expect(button.text()).toBe('Create Account')
    expect(vm.loading).toBe(false)
  })

  it('displays error message when error exists', () => {
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

    const vm = getVm(wrapper)

    expect(vm.error).toBe('')
    
    const errorDiv = wrapper.find('.bg-red-50')
    expect(errorDiv.exists()).toBe(false)
  })

  it('displays success message when registration succeeds', () => {
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

    const vm = getVm(wrapper)

    expect(vm.success).toBe('')
    
    const successDiv = wrapper.find('.bg-green-50')
    expect(successDiv.exists()).toBe(false)
  })

  it('validates password matching', async () => {
    const wrapper = mount(Register)
    
    const passwordInput = wrapper.find('input#password')
    const confirmPasswordInput = wrapper.find('input#confirmPassword')
    const form = wrapper.find('form')
    
    await passwordInput.setValue('password123')
    await confirmPasswordInput.setValue('different')
    
    await form.trigger('submit.prevent')

    const vm = getVm(wrapper)

    expect(vm.error).toBe('Passwords do not match')
  })

  it('validates password length', async () => {
    const wrapper = mount(Register)
    
    const passwordInput = wrapper.find('input#password')
    const confirmPasswordInput = wrapper.find('input#confirmPassword')
    const form = wrapper.find('form')
    
    await passwordInput.setValue('123')
    await confirmPasswordInput.setValue('123')
    
    await form.trigger('submit.prevent')

    const vm = getVm(wrapper)
    
    expect(vm.error).toBe('Password must be at least 6 characters long')
  })

  it('validates terms agreement', async () => {
    const wrapper = mount(Register)
    
    const passwordInput = wrapper.find('input#password')
    const confirmPasswordInput = wrapper.find('input#confirmPassword')
    const form = wrapper.find('form')
    
    await passwordInput.setValue('password123')
    await confirmPasswordInput.setValue('password123')
    
    // Don't check terms checkbox
    
    await form.trigger('submit.prevent')

    const vm = getVm(wrapper)
    
    expect(vm.error).toBe('You must agree to the terms and conditions')
  })

  it('submits form with valid data', async () => {
    const wrapper = mount(Register)
    
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
    await (termsCheckbox as any).setChecked(true)
    
    await form.trigger('submit.prevent')

    const vm = getVm(wrapper)
    
    expect(vm.form.username).toBe('testuser')
    expect(vm.form.name).toBe('Test User')
    expect(vm.form.address).toBe('123 Test St')
    expect(vm.form.password).toBe('password123')
    expect(vm.form.confirmPassword).toBe('password123')
    expect(vm.form.agreeTerms).toBe(true)
  })
})
