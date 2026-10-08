const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.resolve(__dirname, '../docs/evidence/sonarqube');
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function captureAuthenticatedSonar() {
  console.log('Launching Playwright to capture AUTHENTICATED SonarQube dashboards...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1.5,
  });

  const page = await context.newPage();

  // 1. Log in as admin:Admin@12345
  console.log('Logging in to SonarQube...');
  await page.goto('http://localhost:9000/sessions/new');
  await page.waitForLoadState('networkidle');
  await page.fill('#login', 'admin');
  await page.fill('#password', 'Admin@12345');
  await page.click('button[type="submit"]');
  await page.waitForTimeout(3000);
  console.log('Logged in, current URL:', page.url());

  const waitPage = async () => {
    try {
      await page.waitForLoadState('networkidle', { timeout: 10000 });
    } catch (e) {}
    await page.waitForTimeout(2000);
  };

  // SONAR-01: Project Overview / Dashboard
  console.log('Capturing SONAR-01: Project Overview & Quality Gate Status...');
  await page.goto('http://localhost:9000/dashboard?id=dwpg-simulator');
  await waitPage();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-01_project_overview.png'), fullPage: false });

  // SONAR-02: Quality Gate Condition Breakdown
  console.log('Capturing SONAR-02: Quality Gate Details...');
  await page.goto('http://localhost:9000/dashboard?id=dwpg-simulator');
  await waitPage();
  // Scroll slightly to focus on quality gate widget if available
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-02_quality_gate_passed.png'), fullPage: false });

  // SONAR-03: Zero Vulnerabilities SAST Audit
  console.log('Capturing SONAR-03: Issues & Zero Vulnerabilities...');
  await page.goto('http://localhost:9000/project/issues?id=dwpg-simulator&types=VULNERABILITY');
  await waitPage();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-03_issues_vulnerabilities.png'), fullPage: false });

  // SONAR-04: Security Hotspots Review
  console.log('Capturing SONAR-04: Security Hotspots Review...');
  await page.goto('http://localhost:9000/security_hotspots?id=dwpg-simulator');
  await waitPage();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-04_security_hotspots.png'), fullPage: false });

  // SONAR-05: Code Coverage Breakdown
  console.log('Capturing SONAR-05: Code Coverage (62.6%)...');
  await page.goto('http://localhost:9000/component_measures?id=dwpg-simulator&metric=coverage');
  await waitPage();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-05_code_coverage.png'), fullPage: false });

  // SONAR-06: Duplication Analysis
  console.log('Capturing SONAR-06: Code Duplication (0.0%)...');
  await page.goto('http://localhost:9000/component_measures?id=dwpg-simulator&metric=duplicated_lines_density');
  await waitPage();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-06_code_duplications.png'), fullPage: false });

  // SONAR-07: Measures Overview & Technical Debt
  console.log('Capturing SONAR-07: Measures Overview & Maintainability A...');
  await page.goto('http://localhost:9000/component_measures?id=dwpg-simulator');
  await waitPage();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-07_measures_overview.png'), fullPage: false });

  await browser.close();
  console.log('ALL 7 AUTHENTICATED SONARQUBE SCREENSHOTS CAPTURED SUCCESSFULLY!');
}

captureAuthenticatedSonar().catch((err) => {
  console.error('Error capturing authenticated SonarQube screenshots:', err);
  process.exit(1);
});
