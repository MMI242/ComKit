import {MockInstance, vi} from 'vitest'
import { config } from '@vue/test-utils'
import { ref } from 'vue'
import { initApi } from '../services/api'

declare global {
  var vi: any
  var navigateTo: MockInstance
  var definePageMeta: MockInstance
  var defineNuxtRouteMiddleware: any
  var useRuntimeConfig: MockInstance
  var useI18n: MockInstance
}

globalThis.vi = vi
globalThis.navigateTo = vi.fn()
globalThis.definePageMeta = vi.fn()
globalThis.defineNuxtRouteMiddleware = vi.fn(() => ({}))

globalThis.useRuntimeConfig = vi.fn(() => ({
  public: {
    apiBase: 'http://localhost:8000'
  }
}))

// Mock #app imports
globalThis['#app'] = {
  useRuntimeConfig: globalThis.useRuntimeConfig
}

globalThis.useI18n = vi.fn(() => ({
  locale: ref('en'),
  setLocale: vi.fn(),
  t: vi.fn((key: string) => key),
  availableLocales: ['en', 'id']
}))

initApi('http://localhost:8000')

Object.defineProperty(document, 'cookie', {
  writable: true,
  value: 'access_token=mock-token'
})

export const mockFetch = vi.fn()

globalThis.fetch = mockFetch

config.global.stubs = {
  'NuxtLink': {
    template: '<a><slot /></a>',
    props: ['to']
  },
  'NuxtRouteAnnouncer': true,
  'NuxtPage': true,
  'LanguageSwitcher': true,
  'NotificationDropdown': true,
  'BottomNavigation': true,
  'ClientOnly': {
    template: '<div><slot /></div>',
    props: []
  }
}

config.global.mocks = {
  $t: vi.fn((key: string, params?: any) => {
    const translations: Record<string, string> = {
      'auth.login_title': 'Welcome back',
      'auth.login_button': 'Sign in to account',
      'auth.login_subtitle': 'Sign in to your account',
      'auth.email': 'Username',
      'auth.password': 'Password',
      'auth.remember_me': 'Remember me',
      'auth.forgot_password': 'Forgot password?',
      'auth.no_account': "Don't have an account?",
      'auth.register_title': 'Join ComKit',
      'auth.register_subtitle': 'Join ComKit today',
      'auth.full_name': 'Full Name',
      'auth.confirm_password': 'Confirm Password',
      'common.register': 'Sign up now',
      'common.about': 'About',
      'common.terms': 'Terms of Service',
      'common.previous': 'Previous',
      'common.next': 'Next',
      'common.logout': 'Logout',
      'common.loading': 'Loading...',
      'header.welcome': 'Welcome',
      'common.language': 'Language',
      // Special handling for placeholders
      'auth.email_placeholder': 'Enter username',
      'auth.full_name_placeholder': 'John Doe',
      // Dashboard translations
      'dashboard.search_placeholder': 'Cari item...',
      'dashboard.add_item': '+ Add Item',
      'dashboard.add_new_item': '+ Add Item',
      'dashboard.request_item': 'Request Item',
      'dashboard.submitting': 'Submitting...',
      'dashboard.send_request': 'Send Request',
      'dashboard.filter_all': 'All',
      'dashboard.filter_borrow': 'Borrow',
      'dashboard.filter_share': 'Share',
      'dashboard.no_items_found': 'No items found',
      'dashboard.page_info': 'Page {current} of {total} ({items} total items)',
      'dashboard.total_items': '(67 total items)',
      'dashboard.previous': 'Previous',
      'dashboard.next': 'Next',
      'dashboard.available': 'available: 1/1 pcs',
      'dashboard.owner': 'owner: Jqwery Ddo',
      'dashboard.details': 'Details',
      // MyPage translations
      'mypage.my_items': 'Item Saya',
      'mypage.add_new_item': '+ Add New Item',
      'mypage.no_items_shared': 'Belum ada item yang dibagikan',
      'mypage.incoming_requests': 'Request Masuk',
      'mypage.no_incoming_requests': 'Belum ada request masuk',
      'mypage.my_requests': 'Request Saya',
      'mypage.no_outgoing_requests': 'Belum ada request yang dikirim',
      'mypage.qty': 'qty: 1/1 pcs',
      'mypage.type': 'type: borrow',
      'mypage.status': 'status: available',
      'mypage.available': 'available',
      'mypage.borrow': 'borrow',
      'mypage.edit': 'edit',
      'mypage.delete': 'delete',
      'mypage.from': 'from: Jqwery Ddo (jqr123)',
      'mypage.date': 'date: 20/1/2025 - 22/1/2025',
      'mypage.approve': 'approve',
      'mypage.reject': 'reject',
      'mypage.pending': 'Pending',
      'mypage.approved': 'Disetujui',
      'mypage.rejected': 'Ditolak',
      'mypage.approve_action': 'mengupdate',
      'mypage.reject_action': 'Ditolak',
      'mypage.return_action': 'Dikembalikan',
      'mypage.cancel_action': 'Dibatalkan',
      'mypage.returned': 'Dikembalikan',
      'mypage.cancelled': 'Dibatalkan'
    }
    
    let result = translations[key] || key
    
    // Handle parameter interpolation for dashboard.page_info
    if (key === 'dashboard.page_info' && params) {
      result = result
        .replace('{current}', params.current || 1)
        .replace('{total}', params.total || 3)
        .replace('{items}', params.items || 67)
    }
    
    return result
  }),
  $route: {
    path: '/dashboard'
  },
  NuxtRouteAnnouncer: {
    template: '<nuxt-route-announcer-stub></nuxt-route-announcer-stub>'
  },
  NuxtPage: {
    template: '<nuxt-page-stub></nuxt-page-stub>'
  }
}
