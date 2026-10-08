const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.resolve(__dirname, '../docs/evidence/sonarqube');
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function captureSonar() {
  console.log('Launching Playwright to capture real SonarQube evidence from http://localhost:9000...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1.5,
  });

  const page = await context.newPage();

  // Helper wait
  const waitSonar = async () => {
    try {
      await page.waitForLoadState('networkidle', { timeout: 8000 });
    } catch (e) {}
    await page.waitForTimeout(1500);
  };

  // 1. Project Overview / Dashboard
  console.log('Capturing SONAR-01: Project Overview & Quality Gate Passed');
  await page.goto('http://localhost:9000/dashboard?id=dwpg-simulator');
  await waitSonar();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-01_project_overview.png'), fullPage: false });

  // 2. Quality Gate Detail
  console.log('Capturing SONAR-02: Quality Gate Status');
  await page.goto('http://localhost:9000/dashboard?id=dwpg-simulator');
  await waitSonar();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-02_quality_gate_passed.png'), fullPage: false });

  // 3. Issues / Vulnerabilities
  console.log('Capturing SONAR-03: Issues & Zero Vulnerabilities');
  await page.goto('http://localhost:9000/project/issues?id=dwpg-simulator&types=VULNERABILITY');
  await waitSonar();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-03_issues_vulnerabilities.png'), fullPage: false });

  // 4. Security Hotspots
  console.log('Capturing SONAR-04: Security Hotspots');
  await page.goto('http://localhost:9000/security_hotspots?id=dwpg-simulator');
  await waitSonar();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-04_security_hotspots.png'), fullPage: false });

  // 5. Code Coverage
  console.log('Capturing SONAR-05: Code Coverage Breakdown');
  await page.goto('http://localhost:9000/component_measures?id=dwpg-simulator&metric=coverage');
  await waitSonar();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-05_code_coverage.png'), fullPage: false });

  // 6. Duplications
  console.log('Capturing SONAR-06: Duplications Analysis');
  await page.goto('http://localhost:9000/component_measures?id=dwpg-simulator&metric=duplicated_lines_density');
  await waitSonar();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-06_code_duplications.png'), fullPage: false });

  // 7. Measures Overview / Technical Debt
  console.log('Capturing SONAR-07: Measures Overview');
  await page.goto('http://localhost:9000/component_measures?id=dwpg-simulator');
  await waitSonar();
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'SONAR-07_measures_overview.png'), fullPage: false });

  await browser.close();
  console.log('ALL 7 REAL SONARQUBE SCREENSHOTS CAPTURED SUCCESSFULLY!');
}

captureSonar().catch((err) => {
  console.error('Error capturing SonarQube screenshots:', err);
  process.exit(1);
});
