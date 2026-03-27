// @ts-nocheck
const { defineConfig, devices } = require('@playwright/test');
const env = (globalThis && globalThis['process'] && globalThis['process'].env) || {};
const skipWebServer = env.PLAYWRIGHT_SKIP_WEB_SERVER === '1';

/**
 * Local Playwright config for end2end-test so discovery works when running
 * commands directly from this directory.
 */
module.exports = defineConfig({
  testDir: '.',
  testMatch: '**/Test*.js',
  timeout: 60000,
  webServer: skipWebServer
    ? undefined
    : {
        command: 'npm run dev',
        url: 'http://127.0.0.1:8001',
        reuseExistingServer: !env.CI,
        cwd: '../ui',
      },
  forbidOnly: !!env.CI,
  retries: env.CI ? 2 : 0,
  workers: env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['list'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    baseURL: env.BASE_URL || 'http://127.0.0.1:8001',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
});
