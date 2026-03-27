import { test, expect } from '@playwright/test';

// Test configuration
const BASE_URL = process.env.BASE_URL || 'http://localhost:8001';
const API_URL = process.env.API_BASE_URL || 'http://localhost:8000';
const TIMEOUT = 60000;

// Test data - unique username per run
const user1 = {
  name: 'User Satu',
  username: 'user1_' + Date.now(),
  address: 'Jl. Merdeka No. 1, Jakarta Pusat',
  password: 'Password123!'
};

// Helper: wait for Nuxt/Vue hydration so @submit.prevent works
const waitForHydration = async (page) => {
  await page.waitForFunction(() => {
    const nuxtEl = document.getElementById('__nuxt');
    return nuxtEl && nuxtEl.__vue_app__;
  }, { timeout: 30000 });
  // Extra wait to ensure all async plugins/middleware complete
  await page.waitForTimeout(1000);
};

test.describe('Alur Pengguna: Registrasi dan Login', () => {

  test('Fase 1: User1 Registrasi', async ({ page }) => {
    // Navigate to register page
    await page.goto(`${BASE_URL}/register`, { waitUntil: 'load' });

    // Wait for form to be in the DOM
    await page.waitForSelector('#name', { state: 'visible', timeout: TIMEOUT });

    // Wait for Vue hydration (so @submit.prevent is active)
    await waitForHydration(page);

    // Fill register form using element IDs from register.vue
    await page.fill('#name', user1.name);
    await page.fill('#username', user1.username);
    await page.fill('#address', user1.address);
    await page.fill('#password', user1.password);
    await page.fill('#confirmPassword', user1.password);
    await page.check('#agree-terms');

    // Submit registration and wait for the API response
    const [registerResponse] = await Promise.all([
      page.waitForResponse(
        resp => resp.url().includes('/auth/register') && resp.request().method() === 'POST',
        { timeout: TIMEOUT }
      ),
      page.click('button[type="submit"]')
    ]);

    expect(registerResponse.status()).toBe(201);

    // Verify redirect to dashboard
    await page.waitForURL('**/dashboard', { timeout: TIMEOUT });

    // Verify page loaded - TopHeader shows ComKit
    await expect(page.locator('text=ComKit')).toBeVisible({ timeout: TIMEOUT });
  });

  test('Fase 2: User1 Login', async ({ page, request }) => {
    // Ensure user exists via API (handles worker restart on retry where Date.now() changes)
    const ensureUser = await request.post(`${API_URL}/auth/register`, {
      data: {
        username: user1.username,
        password: user1.password,
        name: user1.name,
        address: user1.address
      }
    });
    // 201 = new user created, 409 = already exists from Fase 1 — both are fine
    expect([201, 409]).toContain(ensureUser.status());

    // Navigate to login page
    await page.goto(`${BASE_URL}/login`, { waitUntil: 'load' });

    // Wait for form to be in the DOM
    await page.waitForSelector('#username', { state: 'visible', timeout: TIMEOUT });

    // Wait for Vue hydration (including async plugins/middleware)
    await waitForHydration(page);

    // Fill login form using element IDs from login.vue
    await page.fill('#username', user1.username);
    await page.fill('#password', user1.password);

    // Submit login and wait for the API response
    const [loginResponse] = await Promise.all([
      page.waitForResponse(
        resp => resp.url().includes('/auth/login') && resp.request().method() === 'POST',
        { timeout: TIMEOUT }
      ),
      page.click('button[type="submit"]')
    ]);

    // Verify login API succeeded
    expect(loginResponse.status()).toBe(200);

    // Verify redirect to dashboard
    await page.waitForURL('**/dashboard', { timeout: TIMEOUT });

    // Verify dashboard loaded
    await expect(page.locator('text=ComKit')).toBeVisible({ timeout: TIMEOUT });
  });

});
