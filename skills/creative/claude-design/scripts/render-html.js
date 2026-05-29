#!/usr/bin/env node
/**
 * Render HTML to high-res PNG via headless Chromium (Playwright).
 * Usage: node render-html.js <input.html> [output.png] [scale=2]
 * 
 * Default: 1920x1080 viewport, 2x device scale → 3840x2160 output
 * 
 * Requirements: npm install -g playwright && npx playwright install chromium
 */

const { chromium } = require('playwright');
const path = require('path');

async function main() {
  const inputPath = path.resolve(process.argv[2]);
  const outputPath = path.resolve(process.argv[3] || inputPath.replace(/\.html?$/, '.png'));
  const scale = parseInt(process.argv[4] || '2', 10);

  console.log(`Rendering: ${inputPath}`);
  console.log(`Output:    ${outputPath}`);
  console.log(`Scale:     ${scale}x`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: scale,
  });
  const page = await context.newPage();

  await page.goto(`file://${inputPath}`, { waitUntil: 'networkidle' });
  
  // Wait for fonts + any animations to settle
  await page.waitForTimeout(500);

  await page.screenshot({
    path: outputPath,
    fullPage: false,  // exact viewport
    type: 'png',
  });

  console.log(`✅ Done — ${outputPath} (${Math.round(require('fs').statSync(outputPath).size / 1024)}KB)`);
  await browser.close();
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
