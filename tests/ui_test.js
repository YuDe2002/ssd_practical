const { chromium } = require('playwright');
const https = require('https');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    // Ignore certificate errors because of self-signed cert
    args: ['--ignore-certificate-errors']
  });
  const context = await browser.newContext({
    ignoreHTTPSErrors: true
  });
  const page = await context.newPage();

  // --- Test 1: Weak password (common) should show error ---
  await page.goto('https://localhost/');
  await page.fill('input[name="username"]', 'ui_user');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  // Wait for the error message to appear
  await page.waitForSelector('p[style*="color:red"]', { timeout: 5000 });
  const errorText = await page.textContent('p[style*="color:red"]');
  console.log('Error message:', errorText);
  if (!errorText.toLowerCase().includes('too common') && !errorText.toLowerCase().includes('at least 8')) {
    throw new Error('Expected error message not found');
  }

  // --- Test 2: Strong password should go to welcome page ---
  const strongPass = 'StrongUITest!2024';
  await page.goto('https://localhost/');
  await page.fill('input[name="username"]', 'ui_user2');
  await page.fill('input[name="password"]', strongPass);
  await page.click('button[type="submit"]');
  // Wait for navigation to welcome page
  await page.waitForURL('**/welcome', { timeout: 5000 });
  const pageContent = await page.content();
  if (!pageContent.includes(strongPass)) {
    throw new Error('Password not displayed on welcome page');
  }

  // --- Test 3: Logout clears session and goes back to login ---
  await page.click('a[href*="logout"]');
  await page.waitForURL('**/', { timeout: 5000 });
  const loginForm = await page.$('input[name="password"]');
  if (!loginForm) {
    throw new Error('Not redirected to login page after logout');
  }

  console.log('All UI tests passed!');
  await browser.close();
})();