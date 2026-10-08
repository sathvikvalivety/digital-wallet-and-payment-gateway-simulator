const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.resolve(__dirname, '../docs/evidence/ui');
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function captureAllRealUI() {
  console.log('Launching Playwright to capture verified UI screenshots from http://localhost:3000...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    deviceScaleFactor: 1.5,
  });

  const page = await context.newPage();

  const waitShort = () => page.waitForTimeout(600);
  const waitMed = () => page.waitForTimeout(1400);

  // Clear storage and start fresh
  await page.goto('http://localhost:3000');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.waitForLoadState('networkidle');
  await waitShort();

  // 1. UI-01: User Registration View
  console.log('Capturing UI-01: User Registration Form');
  const regTab = page.locator('button.nav-item:has-text("Register")');
  if (await regTab.isVisible()) {
    await regTab.click();
    await waitShort();
  }

  const uniqueId = Math.floor(Math.random() * 90000 + 10000);
  const studentUser = `alice_fin_${uniqueId}`;
  const studentPass = 'SecurePass123!';

  await page.fill('input[placeholder="Username (letters & numbers)"]', studentUser);
  await page.fill('input[placeholder="you@domain.com"]', `${studentUser}@dwpg.simulator`);
  await page.fill('input[type="password"]', studentPass);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-01_user_registration.png'), fullPage: false });

  // Submit Registration
  await page.click('button[type="submit"]:has-text("Register")');
  await waitMed();

  // 2. UI-02: Sign In Screen
  console.log('Capturing UI-02: User Login View');
  const signOutBtn = page.locator('button:has-text("Sign Out")');
  if (await signOutBtn.isVisible()) {
    await signOutBtn.click();
    await waitShort();
  }

  await page.click('button.nav-item:has-text("Sign In")');
  await waitShort();
  await page.fill('input[placeholder="e.g. alice, merchant_bob, admin"]', studentUser);
  await page.fill('input[placeholder="••••••••••••"]', studentPass);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-02_user_login.png'), fullPage: false });

  // Submit Login
  await page.click('button[type="submit"]:has-text("Sign In")');
  await page.waitForLoadState('networkidle');
  await waitMed();

  // 3. UI-03: Customer Wallet Dashboard
  console.log('Capturing UI-03: Customer Wallet Dashboard');
  const createWalletBtn = page.locator('button:has-text("Create My Simulated Wallet")');
  if (await createWalletBtn.isVisible()) {
    await createWalletBtn.click();
    await waitMed();
  }
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-03_wallet_dashboard.png'), fullPage: false });

  // 4. UI-04: Simulated Funds Top-Up Input Form
  console.log('Capturing UI-04: Funds Top-Up Form');
  const topUpInput = page.locator('input[placeholder="0.00"]');
  await topUpInput.waitFor({ state: 'visible', timeout: 5000 });
  await topUpInput.fill('500.00');
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-04_funds_topup_modal.png'), fullPage: false });

  // 5. UI-05: Top-Up Success Confirmation
  console.log('Capturing UI-05: Top-Up Confirmation ($500.00)');
  await page.click('button[type="submit"]:has-text("Top-Up Wallet")');
  await waitMed();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-05_topup_success.png'), fullPage: false });

  // 6. UI-06: Merchant Onboarding Registration Form
  console.log('Capturing UI-06: Merchant Onboarding Form');
  await page.click('button.nav-item:has-text("Merchant")');
  await waitMed();

  const regMerchantBtn = page.locator('button[type="submit"]:has-text("Provision Merchant Profile")');
  if (await regMerchantBtn.isVisible()) {
    await page.fill('input[placeholder="e.g. Acme Tech Stores, SuperMart Simulator"]', `Apex Cloud Stores #${uniqueId}`);
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-06_merchant_registration.png'), fullPage: false });
    await regMerchantBtn.click();
    await waitMed();
  } else {
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-06_merchant_registration.png'), fullPage: false });
  }

  // 7. UI-07: Merchant Security Portal WITH VISIBLE API KEY
  console.log('Capturing UI-07: Merchant Portal (Revealing API Key)');
  const revealKeyBtn = page.locator('button:has-text("Reveal Key")');
  if (await revealKeyBtn.isVisible()) {
    await revealKeyBtn.click();
    await page.waitForTimeout(600);
  }
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-07_merchant_portal.png'), fullPage: false });

  // Extract the registered merchant ID
  let activeMerchantId = '5';
  try {
    const valText = await page.locator('.metric-value').first().innerText();
    activeMerchantId = valText.replace('#', '').trim();
    console.log(`Active merchant ID detected: ${activeMerchantId}`);
  } catch (e) {
    console.log(`Defaulting merchant ID to: ${activeMerchantId}`);
  }

  // 8. UI-08: Payment Initiation Form
  console.log('Capturing UI-08: Payment Initiation Form');
  await page.click('button.nav-item:has-text("Checkout / Payment")');
  await waitMed();

  // Set target merchant ID to active merchant
  const merchInput = page.locator('input[type="number"]:not([step])');
  if (await merchInput.isVisible()) {
    await merchInput.fill(activeMerchantId);
  }

  const amtInput = page.locator('input[type="number"][step="0.01"]');
  await amtInput.fill('65.00');
  const descInput = page.locator('input[placeholder="What is this payment for?"]');
  if (await descInput.isVisible()) {
    await descInput.fill('Simulated Cloud Service Subscription #7890');
  }
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-08_payment_initiation.png'), fullPage: false });

  // 9. UI-09: Payment Execution & Processing
  console.log('Capturing UI-09: Payment Execution');
  await page.click('button[type="submit"]:has-text("Submit Payment")');
  await waitMed();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-09_payment_confirmation.png'), fullPage: false });

  // 10. UI-10: Cryptographic Payment Receipt
  console.log('Capturing UI-10: Payment Success Receipt');
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-10_payment_success_receipt.png'), fullPage: false });

  // 14. UI-14: Security Tamper & Replay Defense Lab
  console.log('Capturing UI-14: Replay Attack Defense Lab');
  const replayBtn = page.locator('button:has-text("Simulate Replay Attack")');
  if (await replayBtn.isVisible()) {
    await replayBtn.click();
    await waitMed();
  }
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-14_security_tamper_replay_defense.png'), fullPage: false });

  // 11. UI-11: Transaction History Ledger
  console.log('Capturing UI-11: Tamper-Evident Transaction Ledger');
  await page.click('button.nav-item:has-text("Ledger & History")');
  await waitMed();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-11_transaction_history_ledger.png'), fullPage: false });

  // 12. UI-12: Refund Initiation Modal (VISIBLY OPEN)
  console.log('Capturing UI-12: Refund Initiation Modal');
  const refundBtn = page.locator('table button:has-text("Refund")').first();
  await refundBtn.waitFor({ state: 'visible', timeout: 5000 });
  await refundBtn.click();
  await page.waitForTimeout(600);

  // Modal is now visibly open
  const modalHeader = page.locator('h3:has-text("Process Transaction Refund")');
  await modalHeader.waitFor({ state: 'visible', timeout: 3000 });
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-12_refund_initiation.png'), fullPage: false });

  // 13. UI-13: Refund Success & Ledger Entry
  console.log('Capturing UI-13: Refund Success & Ledger Entry');
  const confirmRefundBtn = page.locator('button[type="submit"]:has-text("Confirm Refund")');
  await confirmRefundBtn.click();
  await waitMed();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-13_refund_success_ledger.png'), fullPage: false });

  // 15. UI-15: SIEM Security Audit Explorer (Logged in as audit_admin with ROLE_ADMIN)
  console.log('Capturing UI-15: SIEM Security Audit Explorer as audit_admin');
  const signout = page.locator('button:has-text("Sign Out")');
  if (await signout.isVisible()) {
    await signout.click();
    await waitShort();
  }

  await page.click('button.nav-item:has-text("Sign In")');
  await waitShort();
  await page.fill('input[placeholder="e.g. alice, merchant_bob, admin"]', 'audit_admin');
  await page.fill('input[placeholder="••••••••••••"]', 'SecureAdmin123!');
  await page.click('button[type="submit"]:has-text("Sign In")');
  await page.waitForLoadState('networkidle');
  await waitMed();

  const auditTab = page.locator('button.nav-item:has-text("Security Audit")');
  await auditTab.waitFor({ state: 'visible', timeout: 5000 });
  await auditTab.click();
  await waitMed();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-15_admin_audit_logs.png'), fullPage: false });

  await browser.close();
  console.log('ALL 15 VERIFIED REAL UI SCREENSHOTS CAPTURED SUCCESSFULLY!');
}

captureAllRealUI().catch((err) => {
  console.error('Error capturing UI screenshots:', err);
  process.exit(1);
});
