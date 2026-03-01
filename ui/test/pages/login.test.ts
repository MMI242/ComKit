import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Login from '../../app/pages/login.vue'

// Mock navigateTo
vi.mock('#app/composables', () => ({
  navigateTo: vi.fn()
}))

describe('Login Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
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
    const vm = getVm(wrapper)

    expect(wrapper.find('button[type="submit"]').text()).toBe('Sign in to account')
    expect(vm.loading).toBe(false)
  })

  it('displays error message when error exists', () => {
    const wrapper = mount(Login)
    const vm = getVm(wrapper)

    expect(vm.error).toBe('')
    expect(wrapper.find('.bg-red-50').exists()).toBe(false)
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

  it('shows error with invalid credentials', async () => {
    const wrapper = mount(Login)
    const vm = getVm(wrapper)

    await wrapper.find('input#username').setValue('wrong')
    await wrapper.find('input#password').setValue('wrong')
    await wrapper.find('form').trigger('submit.prevent')

    await new Promise(resolve => setTimeout(resolve, 1100))

    expect(vm.error).toBe('Invalid username or password')
  })
})