import { chromium } from 'playwright'

const browser = await chromium.launch({ headless: true })
const page = await browser.newPage()
await page.setViewportSize({ width: 1440, height: 900 })

const shots = (name) => `c:/Users/venkatas/Projects-code/3x-agent-creation/blast-agent/.tmp/${name}.png`

// Screen 1: Connect form
await page.goto('http://localhost:5173', { waitUntil: 'networkidle' })
await page.waitForSelector('text=Connect to Figma', { timeout: 10000 })
await page.screenshot({ path: shots('01-connect') })
console.log('01-connect.png captured')

// Click generate
await page.click('button:has-text("Fetch & Generate")')

try {
  await page.waitForSelector('text=Test Plan Sections', { timeout: 20000 })
  await page.screenshot({ path: shots('02-dashboard') })
  console.log('02-dashboard.png captured')

  // UI Test Cases (default)
  await page.screenshot({ path: shots('03-ui-tests') })
  console.log('03-ui-tests.png captured')

  // Functional
  await page.click('button:has-text("Functional")')
  await page.waitForTimeout(400)
  await page.screenshot({ path: shots('04-functional') })
  console.log('04-functional.png captured')

  // Compatibility
  await page.click('button:has-text("Compatibility")')
  await page.waitForTimeout(400)
  await page.screenshot({ path: shots('05-compat') })
  console.log('05-compat.png captured')

  // Sign-off
  await page.click('button:has-text("Sign-off")')
  await page.waitForTimeout(400)
  await page.screenshot({ path: shots('06-signoff') })
  console.log('06-signoff.png captured')

} catch (e) {
  await page.screenshot({ path: shots('error') })
  console.error('ERROR:', e.message)
}

await browser.close()
console.log('Done')
