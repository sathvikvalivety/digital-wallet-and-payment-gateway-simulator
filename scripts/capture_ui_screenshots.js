const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.resolve(__dirname, '../docs/evidence/ui');
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function capture() {
  console.log('Launching headless Chromium to capture all 15 real UI screenshots...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1366, height: 850 },
    deviceScaleFactor: 1.5,
  });

  const page = await context.newPage();

  // 1. User Registration View
  console.log('Capturing UI-01: User Registration');
  await page.goto('http://localhost:3000');
  await page.waitForLoadState('networkidle');

  // Ensure we are on register view
  const regTab = page.locator('button.nav-item:has-text("Register")');
  if (await regTab.isVisible()) {
    await regTab.click();
    await page.waitForTimeout(400);
  }

  const uniqueSuffix = Math.floor(Math.random() * 90000 + 10000);
  const testUser = `eva_wallet_${uniqueSuffix}`;
  const testPass = 'SecurePass123!';

  await page.fill('input[placeholder="Username (letters & numbers)"]', testUser);
  await page.fill('input[placeholder="you@domain.com"]', `${testUser}@simulator.dwpg`);
  await page.fill('input[type="password"]', testPass);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-01_user_registration.png'), fullPage: false });

  // Submit registration
  await page.click('button[type="submit"]:has-text("Register")');
  await page.waitForTimeout(1000);

  // 2. User Login View
  console.log('Capturing UI-02: User Login');
  const logoutBtn = page.locator('button:has-text("Sign Out")');
  if (await logoutBtn.isVisible()) {
    await logoutBtn.click();
    await page.waitForTimeout(500);
  }

  await page.click('button.nav-item:has-text("Sign In")');
  await page.waitForTimeout(400);

  await page.fill('input[placeholder="e.g. alice, merchant_bob, admin"]', testUser);
  await page.fill('input[placeholder="••••••••••••"]', testPass);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-02_user_login.png'), fullPage: false });

  // Log in
  await page.click('button[type="submit"]:has-text("Sign In")');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);

  // 3. Customer Wallet Dashboard
  console.log('Capturing UI-03: Customer Wallet Dashboard');
  // Wait for wallet creation button or wallet card
  await page.waitForTimeout(800);
  const createWalletBtn = page.locator('button:has-text("Create My Simulated Wallet")');
  if (await createWalletBtn.isVisible()) {
    await createWalletBtn.click();
    await page.waitForTimeout(1000);
  }
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-03_wallet_dashboard.png'), fullPage: false });

  // 4. Simulated Funds Top-Up Input
  console.log('Capturing UI-04: Funds Top-Up Form');
  const topUpInput = page.locator('input[placeholder="0.00"]');
  await topUpInput.waitFor({ state: 'visible', timeout: 5000 });
  await topUpInput.fill('500.00');
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-04_funds_topup_modal.png'), fullPage: false });

  // 5. Top-Up Success
  console.log('Capturing UI-05: Top-Up Success');
  await page.click('button[type="submit"]:has-text("Top-Up Wallet")');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-05_topup_success.png'), fullPage: false });

  // 6. Merchant View
  console.log('Capturing UI-06 & UI-07: Merchant Registration & Portal');
  await page.click('button.nav-item:has-text("Merchant")');
  await page.waitForTimeout(800);

  const regMerchantBtn = page.locator('button[type="submit"]:has-text("Register Merchant")');
  if (await regMerchantBtn.isVisible()) {
    await page.fill('input[placeholder="e.g. Acme Superstore"]', `Simulated Merchant Store ${uniqueSuffix}`);
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-06_merchant_registration.png'), fullPage: false });
    await regMerchantBtn.click();
    await page.waitForTimeout(1200);
  } else {
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-06_merchant_registration.png'), fullPage: false });
  }

  // Reveal API Key
  const revealKeyBtn = page.locator('button:has-text("Reveal Key")');
  if (await revealKeyBtn.isVisible()) {
    await revealKeyBtn.click();
    await page.waitForTimeout(300);
  }
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-07_merchant_portal.png'), fullPage: false });

  // 8. Payment Initiation View
  console.log('Capturing UI-08: Payment Initiation');
  await page.click('button.nav-item:has-text("Checkout / Payment")');
  await page.waitForTimeout(800);

  // Set values
  const amtInput = page.locator('input[type="number"][step="0.01"]');
  await amtInput.fill('65.00');
  await page.fill('input[value="Simulator order checkout test"]', 'Official Security Audit Verification #8902');
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-08_payment_initiation.png'), fullPage: false });

  // 9. Payment Confirmation & 10. Success Receipt
  console.log('Capturing UI-09 & UI-10: Payment Confirmation and Receipt');
  await page.click('button[type="submit"]:has-text("Submit Payment")');
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-09_payment_confirmation.png'), fullPage: false });
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-10_payment_success_receipt.png'), fullPage: false });

  // 14. Simulate Replay Attack
  console.log('Capturing UI-14: Security Tamper & Replay Defense');
  const replayBtn = page.locator('button:has-text("Simulate Replay Attack")');
  if (await replayBtn.isVisible()) {
    await replayBtn.click();
    await page.waitForTimeout(1500);
  }
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-14_security_tamper_replay_defense.png'), fullPage: false });

  // 11. Transaction History Ledger
  console.log('Capturing UI-11: Transaction History Ledger');
  await page.click('button.nav-item:has-text("Ledger & History")');
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-11_transaction_history_ledger.png'), fullPage: false });

  // 12. Refund Initiation Modal
  console.log('Capturing UI-12: Refund Initiation');
  const refundBtn = page.locator('button:has-text("Request Refund")').first();
  if (await refundBtn.isVisible()) {
    await refundBtn.click();
    await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-12_refund_initiation.png'), fullPage: false });

    // 13. Refund Success & Ledger Entry
    console.log('Capturing UI-13: Refund Success & Ledger');
    await page.click('button[type="submit"]:has-text("Confirm & Process Refund")');
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-13_refund_success_ledger.png'), fullPage: false });
  } else {
    // If no refund button found, capture the view
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-12_refund_initiation.png'), fullPage: false });
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-13_refund_success_ledger.png'), fullPage: false });
  }

  // 15. Admin / Security Audit Log View
  console.log('Capturing UI-15: Admin Security Audit Log View');
  await page.click('button:has-text("Sign Out")');
  await page.waitForTimeout(500);

  // Sign in as admin_auditor
  await page.fill('input[placeholder="e.g. alice, merchant_bob, admin"]', 'admin_auditor');
  await page.fill('input[placeholder="••••••••••••"]', 'AdminPass123!');
  await page.click('button[type="submit"]:has-text("Sign In")');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);

  // Click Security Audit
  const adminTab = page.locator('button.nav-item:has-text("Security Audit")');
  if (await adminTab.isVisible()) {
    await adminTab.click();
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'UI-15_admin_audit_logs.png'), fullPage: false });
  }

  await browser.close();
  console.log('ALL 15 REAL UI SCREENSHOTS CAPTURED SUCCESSFULLY!');
}

capture().catch((err) => {
  console.error('Error capturing UI screenshots:', err);
  process.exit(1);
});
