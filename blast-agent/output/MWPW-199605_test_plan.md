# Test Plan — MWPW-199605
## Firefly Remove Background — SEO Page Functionality

| Field      | Value                              |
|------------|------------------------------------|
| Ticket     | MWPW-199605                        |
| Status     | Draft                              |
| Priority   | Normal                             |
| Assignee   | Sigadam Venkata Ramesh             |
| Reporter   | Sigadam Venkata Ramesh             |
| Generated  | 2026-06-24                         |

---

## 1. Objective

Verify that the Adobe Firefly "Remove Background" SEO landing page at  
`https://www.adobe.com/products/firefly/features/remove-background.html`  
functions correctly and completely — covering Global Navigation CTAs, the marquee section with animation and image upload, file format and size validation, the accordion feature block, and cross-browser / cross-OS compatibility.

This is a high-traffic, high-visibility page. Any defect has direct impact on user acquisition and SEO performance.

---

## 2. Scope

### In Scope
- Page load and rendering across supported browsers and OS
- Global Navigation — Login CTA and Firefly navigation CTA
- Marquee section — title, branding, and remove-background animation
- Unity image upload block — supported formats (JPG, PNG)
- Image upload error handling — unsupported formats and files exceeding 40 MB
- Accordion block — "How to remove a background with Adobe Firefly"
- Responsive rendering — desktop, tablet, mobile
- Basic SEO elements — page title, meta description, H1

### Out of Scope
- Backend remove-background AI processing quality
- Payment / subscription flows
- Full A.com regression
- Performance and load testing
- Accessibility deep-dive audit (separate ticket)

---

## 3. Test Strategy

**Approach:** Manual functional testing with cross-browser and cross-OS coverage.

**Test execution order:**
1. Verify page loads correctly and SEO elements are present
2. Validate Global Navigation CTAs
3. Test marquee — title, animation, and image upload (happy path)
4. Test image upload error cases (wrong format, oversized)
5. Verify accordion block content and interaction
6. Repeat across all target browsers and OS combinations

---

## 4. Entry Criteria

- [ ] Page is live at `https://www.adobe.com/products/firefly/features/remove-background.html`
- [ ] Test image assets prepared: valid JPG (< 40 MB), valid PNG (< 40 MB), invalid format (e.g. PDF, GIF, BMP, TIFF), oversized image (> 40 MB)
- [ ] Test accounts available (logged-in and logged-out states)
- [ ] All target browsers installed (Chrome, Safari, Firefox, Edge — latest versions)

---

## 5. Exit Criteria

- [ ] All test cases executed across desktop, tablet, and mobile
- [ ] All Critical and High defects resolved or accepted with a known workaround
- [ ] Cross-browser smoke tests passed (Chrome, Safari, Firefox, Edge)
- [ ] Sign-off from assignee (Sigadam Venkata Ramesh)

---

## 6. Test Environment

| Item             | Detail                                                                                  |
|------------------|-----------------------------------------------------------------------------------------|
| Page URL         | https://www.adobe.com/products/firefly/features/remove-background.html                  |
| Browsers         | Chrome (latest), Safari (latest), Firefox (latest), Edge (latest)                       |
| Operating Systems| Windows 11, macOS (latest), iOS (latest), Android (latest)                              |
| Viewports        | Desktop 1440px+, Tablet 768px–1024px, Mobile 375px–767px                                |
| Test Images      | Valid JPG < 40 MB, Valid PNG < 40 MB, PDF / BMP / GIF (invalid), Image > 40 MB (invalid)|

---

## 7. Test Image Preparation

| File | Type | Size | Expected outcome |
|---|---|---|---|
| valid_small.jpg | JPG | 2 MB | Upload accepted |
| valid_small.png | PNG | 3 MB | Upload accepted |
| valid_large.jpg | JPG | 39 MB | Upload accepted (boundary) |
| oversized.jpg | JPG | 41 MB+ | Error shown to user |
| test.pdf | PDF | any | Error shown to user |
| test.gif | GIF | any | Error shown to user |
| test.bmp | BMP | any | Error shown to user |

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Page content changes during testing | Medium | High | Lock page content before test execution; note version/date |
| Upload block requires auth / entitlement | Medium | High | Test both logged-in and logged-out states |
| Animation not visible in headless / low-power mode | Low | Medium | Test on physical device or standard browser (not headless) |
| 40 MB limit enforced client-side only | Medium | Medium | Test with large file to confirm UI error appears before any server call |
| Cross-OS font rendering differences | Low | Low | Document as known cosmetic variation, not a defect |
