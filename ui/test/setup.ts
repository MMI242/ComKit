import {MockInstance, vi} from 'vitest'
import { config } from '@vue/test-utils'
import { initApi } from '../services/api'

declare global {
  var vi: any
  var navigateTo: MockInstance
  var definePageMeta: MockInstance
  var defineNuxtRouteMiddleware: any
  var useRuntimeConfig: MockInstance
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

initApi('http://localhost:8000')

Object.defineProperty(document, 'cookie', {
  writable: true,
  value: 'access_token=mock-token'
})

export const mockFetch = vi.fn()

globalThis.fetch = mockFetch

config.global.stubs = {
  'NuxtLink': true,
  'NuxtRouteAnnouncer': true,
  'NuxtPage': true,
  'ClientOnly': {
    template: '<div><slot /></div>',
    props: []
  }
}

config.global.mocks = {
  NuxtRouteAnnouncer: {
    template: '<nuxt-route-announcer-stub></nuxt-route-announcer-stub>'
  },
  NuxtPage: {
    template: '<nuxt-page-stub></nuxt-page-stub>'
  }
}
