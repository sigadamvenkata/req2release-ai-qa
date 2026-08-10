# Test Plan — Adobe LLM Optimizer Landing Page
**Source:** Figma — venkata-fullpage1 (homepage canvas)
**Figma File:** Ke7YGOv0lTVJeVZw33mLT2 | Last Modified: 2026-04-16
**Generated:** 2026-07-03
**Page Dimensions:** 1920 × 4301 px (desktop)

---

## 1. Objective

Validate that the Adobe LLM Optimizer landing page renders correctly, all interactive components function as designed, content is accurate, and the page is responsive across desktop, tablet and mobile viewports — matching the Figma specification exactly.

---

## 2. Scope

### In Scope
| Area | Details |
|---|---|
| Global Navigation | Mega-nav: Creative Cloud products, Featured products, Explore categories, Sign In, phone number |
| Hero Section | Headline, body copy, dual CTAs (Watch Overview / Take a tour), countdown timer, QR code, background media |
| Feature Blocks (×3) | AI search presence, content optimisation, business impact — copy, bullet features, CTAs, countdown timers, media images |
| FAQ / Accordion | 10 FAQ items, expand/collapse behaviour |
| Contact / CTA Section | Heading, "Get started" + "Learn more" CTAs |
| Global Footer | All product links, business/education/nonprofit/mobile categories, copyright, legal links |
| Responsive Layout | Desktop (1920px), Tablet (768px), Mobile (375px) |
| Accessibility | Alt text on images, keyboard nav, contrast ratios |
| Performance | Page load time, image optimisation |
| Cross-browser | Chrome, Firefox, Safari, Edge |

### Out of Scope
- Backend / API integrations behind CTAs
- User authentication flows
- Analytics tracking (data layer events)
- A/B test variant logic
- CMS authoring interface

---

## 3. Page Sections (from Figma)

```
1. Global Header / Navigation
2. Hero Section             — Adobe LLM Optimizer product launch
3. Feature Block A          — "Own your presence within AI search and discovery."
4. Feature Block B          — "Optimize and deploy content for increased AI search performance."
5. Feature Block C          — "Connect AI-driven traffic to measurable growth."
6. FAQ Accordion            — "Questions? We have answers." (10 FAQs)
7. Contact / CTA Banner     — "Let's talk about what Adobe LLM Optimizer can do for your business."
8. Global Footer
```

---

## 4. Test Strategy

| Layer | Approach | Tools |
|---|---|---|
| Visual / Layout | Compare rendered page against Figma frame (1920px) | Playwright screenshots + visual diff |
| Functional | Click, hover, expand, form interactions | Playwright automation |
| Content | Verify all text strings match Figma spec | Playwright text assertions |
| Responsive | Resize to 768px (tablet) and 375px (mobile) | Playwright viewport |
| Accessibility | Alt text, ARIA roles, keyboard tab order | axe-playwright |
| Cross-browser | Chrome, Firefox, Safari, Edge | Playwright multi-browser |
| Performance | LCP, CLS, FCP, TTI | Lighthouse / Web Vitals |

---

## 5. Entry / Exit Criteria

### Entry
- [ ] Staging URL accessible (HTTP 200)
- [ ] All Figma-specified sections present in DOM
- [ ] No console errors on page load
- [ ] Playwright browsers installed

### Exit
- [ ] All @critical tests pass
- [ ] No P1/P2 visual regressions vs Figma
- [ ] Cross-browser tests complete (Chrome + Firefox + Safari)
- [ ] All failures documented with Jira tickets

---

## 6. Test Environment

| Env | Viewport | Notes |
|---|---|---|
| Desktop | 1920 × 1080 | Matches Figma frame |
| Tablet | 768 × 1024 | iPad portrait |
| Mobile | 375 × 812 | iPhone portrait |
| Mobile Landscape | 812 × 375 | iPhone landscape |

**Browsers:** Chrome 125+, Firefox 127+, Safari/WebKit 17+, Edge 125+

---

## 7. Test Case Groups

| # | Group | Tag | Scenarios | Priority |
|---|---|---|---|---|
| 1 | Global Navigation | @ui @nav | 8 | High |
| 2 | Hero Section | @ui @hero | 7 | Critical |
| 3 | Feature Block A — AI Search Presence | @ui @feature | 5 | High |
| 4 | Feature Block B — Content Optimisation | @ui @feature | 5 | High |
| 5 | Feature Block C — Business Impact | @ui @feature | 5 | High |
| 6 | FAQ Accordion | @ui @accordion | 6 | High |
| 7 | Contact / CTA Banner | @ui @cta | 3 | Medium |
| 8 | Global Footer | @ui @footer | 6 | Medium |
| 9 | Responsive Layout | @responsive | 6 | High |
| 10 | Accessibility | @a11y | 5 | Medium |
| 11 | Performance | @perf | 3 | Medium |
| 12 | Cross-Browser | @compat | 4 | High |
| **Total** | | | **63** | |

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Countdown timer shows wrong values | Medium | High | Assert timer units (DAYS/HOURS/MINS) are visible; value tested separately |
| QR code image missing/broken | Low | Medium | Assert image src non-empty and 200 status |
| FAQ accordion JS not loading | Medium | High | Assert each accordion item expands/collapses |
| Figma placeholder text shipped to prod | Medium | High | Assert no "Lorem ipsum", "Body ipsum", or "Alt text" strings in live content |
| Footer links returning 404 | Low | Medium | Spot-check key footer links (privacy, terms, products) |
| Mobile nav hamburger not functional | Medium | High | Test hamburger open/close on 375px viewport |
| Hero background image not loading on mobile | Medium | High | Assert background-image or img src on mobile viewport |
| Locale modal blocking hero content | High | High | Dismiss modal before asserting any content |
