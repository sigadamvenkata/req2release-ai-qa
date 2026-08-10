# Test Cases — Adobe LLM Optimizer Landing Page
**Source:** Figma — venkata-fullpage1 (homepage canvas)
**Format:** Gherkin BDD
**Generated:** 2026-07-03

---

## Feature: Global Navigation

### Scenario 1.1: Global nav renders with Creative Cloud mega-menu
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the global header
Then the Adobe logo should be visible
And "What is Creative Cloud?" link should be present
And "Photographers" link should be present
And "Students and Teachers" link should be present
And "Small and medium business" link should be present
And "Enterprise" link should be present
```

### Scenario 1.2: Nav shows sign in and phone number
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the top navigation bar
Then the "Sign in" button should be visible
And the phone number "1-800-685-4193" should be visible
```

### Scenario 1.3: "View plans and pricing" link is present
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I view the Creative Cloud nav section
Then "View plans and pricing" link should be present and clickable
```

### Scenario 1.4: Featured products section shows all six products
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I open the navigation's Featured products panel
Then the following products should be listed:
  | Product         | Description                             |
  | Photoshop       | Image editing and design                |
  | Lightroom       | The cloud-based photo service           |
  | Illustrator     | Vector graphics and illustration        |
  | Premiere Pro    | Video editing and production            |
  | Adobe Acrobat   | The complete PDF solution               |
  | Adobe Stock     | High-quality licensable assets          |
And "View all Creative Cloud products" link should be present
```

### Scenario 1.5: Explore categories visible in navigation
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I view the Explore section of the navigation
Then the following categories should be present:
  | Photo | Graphic design | Video | Illustration |
  | UI and UX | Social media | 3D and AR |
```

### Scenario 1.6: Breadcrumb navigation renders correctly
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the breadcrumb
Then "Home" should be the first breadcrumb item
And "/" separator should be present
And "Current Page" should be the last breadcrumb item
```

### Scenario 1.7: Navigation is sticky on scroll
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I scroll down past the hero section
Then the global navigation bar should remain fixed at the top of the viewport
```

### Scenario 1.8: Mobile hamburger menu opens and closes
```gherkin
Given the viewport is set to 375x812 (mobile portrait)
And the Adobe LLM Optimizer landing page is open
When I tap the hamburger menu icon
Then the navigation panel should expand and show all menu items
When I tap the close button
Then the navigation panel should collapse
```

---

## Feature: Hero Section

### Scenario 2.1: Hero product logo and brand name are visible
```gherkin
Given the Adobe LLM Optimizer landing page is open
When the hero section is in view
Then the Adobe product lockup logo should be visible
And the brand name "Adobe" should be displayed
And the product name "Adobe LLM Optimizer" should be visible as a heading
```

### Scenario 2.2: Hero heading text matches Figma spec
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I read the hero heading (Heading XL/XXXL)
Then the text should be "Drive brand authority in AI search and discovery."
```

### Scenario 2.3: Hero body copy is present and non-empty
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I read the hero body text (Body XL)
Then the text should contain "Shape how your brand shows up in AI search results"
And the text should not contain "Lorem ipsum" or "Body ipsum" placeholder text
```

### Scenario 2.4: Hero CTAs "Watch Overview" and "Take a tour" are present
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look for call-to-action buttons in the hero
Then a primary button labelled "Watch Overview" should be visible
And a secondary button labelled "Take a tour" should be visible
And both buttons should be clickable
```

### Scenario 2.5: Countdown timer is visible with correct units
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the countdown timer in the hero section
Then the label "ENDS IN" should be visible
And "DAYS" unit label should be visible
And "HOURS" unit label should be visible
And "MINS" unit label should be visible
And numeric digit placeholders should be visible for each unit
```

### Scenario 2.6: QR code section renders correctly
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the hero QR code area
Then the QR code image should be visible and not broken
And "Download on the" text should be visible
And "get it on" text should be visible
```

### Scenario 2.7: Hero background media loads correctly
```gherkin
Given the Adobe LLM Optimizer landing page is open at 1920px desktop viewport
When the hero section renders
Then the background image (desktop) should load without a broken image icon
And the 16:9 ratio media element should be visible
And the alt text attribute should not be empty
```

---

## Feature: Feature Block A — AI Search Presence

### Scenario 3.1: Feature Block A heading matches Figma spec
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I scroll to the first feature block
Then the heading should read "Own your presence within AI search and discovery."
And the subheading body text should contain "Ensure your brand, products, and content are visible"
```

### Scenario 3.2: Feature Block A shows three capability bullet points
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I read the Feature Block A bullet features
Then the following text fragments should be present:
  | "Understand where and how often your content appears in AI search results" |
  | "Get generative engine optimization (GEO) scores" |
  | "Track your AI search share-of-voice and AI-driven citations against competitors" |
```

### Scenario 3.3: Feature Block A "Learn more" CTAs are clickable
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I locate the "Learn more" buttons in Feature Block A
Then at least one "Learn more" link should be visible
And clicking it should not result in a 404 error page
```

### Scenario 3.4: Feature Block A media image loads correctly
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the 4:3 media image in Feature Block A
Then the image should be visible and not broken
And the image alt text should not be empty
```

### Scenario 3.5: Feature Block A countdown timer is visible
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the countdown timer in Feature Block A
Then the "ENDS IN" label, DAYS, HOURS, and MINS units should all be visible
```

---

## Feature: Feature Block B — Content Optimisation

### Scenario 4.1: Feature Block B heading matches Figma spec
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I scroll to the second feature block
Then the heading should read "Optimize and deploy content for increased AI search performance."
And the body text should contain "Move from insight to action with prescriptive recommendations"
```

### Scenario 4.2: Feature Block B shows four capability bullet points
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I read the Feature Block B bullet features
Then the following text fragments should be present:
  | "Automatically get actionable suggestions for fixing technical issues" |
  | "Optimize the on-site content and off-site sources that LLMs rely on" |
  | "Seamlessly publish updates with a single click using Adobe Experience Manager" |
  | "Securely integrate into enterprise ecosystems using standards such as Agent2Agent (A2A) and Model Context Protocol (MCP)" |
```

### Scenario 4.3: Feature Block B "Learn more" CTAs are clickable
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I locate the "Learn more" buttons in Feature Block B
Then at least one "Learn more" link should be visible and clickable
```

### Scenario 4.4: Feature Block B media image loads correctly
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the 4:3 media image in Feature Block B
Then the image should be visible and not broken
```

### Scenario 4.5: Feature Block B countdown timer is visible
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the countdown timer in Feature Block B
Then DAYS, HOURS, and MINS labels should all be visible
```

---

## Feature: Feature Block C — Business Impact

### Scenario 5.1: Feature Block C heading matches Figma spec
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I scroll to the third feature block
Then the heading should read "Connect AI-driven traffic to measurable growth."
And the body text should contain "Quantify the total business impact of your brand's presence across AI channels"
```

### Scenario 5.2: Feature Block C shows four capability bullet points
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I read the Feature Block C bullet features
Then the following text fragments should be present:
  | "Map AI-driven visibility to user behavior and business performance" |
  | "Out-of-the-box reporting allows teams to quickly share insights" |
  | "Projected traffic value in dollars helps teams prioritize" |
  | "Securely integrate into enterprise ecosystems using standards such as Agent2Agent (A2A)" |
```

### Scenario 5.3: Feature Block C "Learn more" CTAs are clickable
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I locate the "Learn more" buttons in Feature Block C
Then at least one "Learn more" link should be visible and clickable
```

### Scenario 5.4: Feature Block C media image loads correctly
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the 4:3 media image in Feature Block C
Then the image should be visible and not broken
```

### Scenario 5.5: Feature Block C countdown timer is visible
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the countdown timer in Feature Block C
Then DAYS, HOURS, and MINS labels should all be visible
```

---

## Feature: FAQ Accordion

### Scenario 6.1: FAQ section heading is visible
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I scroll to the FAQ section
Then the heading "Questions? We have answers." should be visible
```

### Scenario 6.2: All 10 FAQ items are present
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the FAQ accordion
Then the following 10 questions should be listed:
  | "What is Adobe LLM Optimizer?" |
  | "What problem does Adobe LLM Optimizer solve?" |
  | "Who is Adobe LLM Optimizer for?" |
  | "How does Adobe LLM Optimizer work?" |
  | "What makes Adobe LLM Optimizer different from traditional SEO tools?" |
  | "What is an LLM?" |
  | "What are examples of LLMs used in marketing and search?" |
  | "Why do LLMs matter for digital marketers and content teams?" |
  | "Can I use Adobe LLM Optimizer without Adobe Experience Manager?" |
  | "Does Adobe LLM Optimizer measure traffic from LLMs?" |
```

### Scenario 6.3: First FAQ item expands to show answer
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I click on "What is Adobe LLM Optimizer?"
Then the answer panel should expand and be visible
And the answer should contain "generative AI search and discovery optimization solution"
And "Learn more" link should be visible within the expanded answer
```

### Scenario 6.4: Expanded FAQ item collapses when clicked again
```gherkin
Given the "What is Adobe LLM Optimizer?" FAQ item is expanded
When I click on the same FAQ item again
Then the answer panel should collapse and become hidden
```

### Scenario 6.5: Only one FAQ item can be expanded at a time
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I expand "What is Adobe LLM Optimizer?"
And I then click "What problem does Adobe LLM Optimizer solve?"
Then "What problem does Adobe LLM Optimizer solve?" should be expanded
And "What is Adobe LLM Optimizer?" should be collapsed
```

### Scenario 6.6: FAQ section media image loads correctly
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the 4:3 image within the first FAQ answer
Then the image should be visible and not broken
And the image alt text should not be empty
```

---

## Feature: Contact / CTA Banner

### Scenario 7.1: CTA banner heading matches Figma spec
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I scroll to the CTA contact banner
Then the heading should read "Let's talk about what Adobe LLM Optimizer can do for your business."
```

### Scenario 7.2: "Get started" primary CTA is visible and clickable
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the CTA banner
Then the "Get started" button should be visible
And clicking it should not produce a 404 error
```

### Scenario 7.3: "Learn more" secondary CTA is visible alongside primary CTA
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the CTA banner
Then both "Get started" and "Learn more" buttons should be visible
And both should be interactive
```

---

## Feature: Global Footer

### Scenario 8.1: Footer renders all product category columns
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I scroll to the global footer
Then the following "Shop for" product links should be visible:
  | Creative Cloud | Photoshop | Adobe Express | Photography |
  | Premiere Pro | Adobe Stock | Elements Family |
And "View plans and pricing" and "View all products" links should be present
```

### Scenario 8.2: Footer business, education and nonprofit sections are present
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the footer columns
Then "For business" section should show "Creative Cloud for business" and "Acrobat for Business"
And "For education" section should show "Discounts for students and teachers"
And "For nonprofits" section should show "Nonprofit overview"
```

### Scenario 8.3: Footer Experience Cloud products are listed
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the footer Experience Cloud section
Then the following products should be listed:
  | Analytics | Experience Manager | Commerce | Marketo Engage | Workfront |
```

### Scenario 8.4: Footer legal links are present
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the bottom footer bar
Then "Privacy" link should be visible
And "Terms of Use" link should be visible
And "Cookie preferences" link should be visible
And "Do not sell my personal information" link should be visible
And "AdChoices" link should be visible
And the copyright text "Copyright © 2025 Adobe. All rights reserved." should be present
```

### Scenario 8.5: Footer company section is present
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I inspect the Company footer column
Then the following links should be present:
  | About Adobe | AI Overview | Careers | Newsroom |
  | Corporate responsibility | Investor Relations | Trust Center |
```

### Scenario 8.6: Footer "Change region" link is visible
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I look at the footer
Then "Change region" link should be visible
```

---

## Feature: Responsive Layout

### Scenario 9.1: Page renders correctly at desktop 1920px
```gherkin
Given the viewport is set to 1920x1080 (desktop)
And the Adobe LLM Optimizer landing page is open
When I inspect the layout
Then all 8 page sections should be visible in the correct order
And no content should overflow horizontally
```

### Scenario 9.2: Page renders correctly at tablet 768px
```gherkin
Given the viewport is set to 768x1024 (tablet)
And the Adobe LLM Optimizer landing page is open
When I inspect the layout
Then the hero section, all feature blocks, FAQ, CTA and footer should be visible
And no horizontal scroll should occur
And the global navigation should adapt to tablet layout
```

### Scenario 9.3: Page renders correctly at mobile 375px portrait
```gherkin
Given the viewport is set to 375x812 (mobile portrait)
And the Adobe LLM Optimizer landing page is open
When I inspect the layout
Then all page sections should stack vertically
And no horizontal overflow should occur (scrollWidth <= innerWidth)
And the hamburger menu icon should be visible
```

### Scenario 9.4: Page renders correctly at mobile 812px landscape
```gherkin
Given the viewport is set to 812x375 (mobile landscape)
And the Adobe LLM Optimizer landing page is open
When the page renders
Then all sections should be accessible without horizontal overflow
```

### Scenario 9.5: Feature block images switch from background to regular image on tablet/mobile
```gherkin
Given the viewport is set to 768x1024 (tablet)
When the hero section renders
Then the tablet/mobile image (not background) version should be used
And the image should load correctly with a valid src
```

### Scenario 9.6: No placeholder text visible on any viewport
```gherkin
Given the landing page is open at 1920px, 768px, and 375px
When I scan all visible text content
Then no text should contain "Lorem ipsum" or "Body ipsum"
And no image alt text should be literally "Alt text"
And no text should be "{Setting 2}"
```

---

## Feature: Accessibility

### Scenario 10.1: All images have non-empty alt attributes
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I audit all img elements on the page
Then every img should have an alt attribute
And no alt attribute should be literally "Alt text" (Figma placeholder)
And no alt attribute should be null or empty for informational images
```

### Scenario 10.2: Heading hierarchy follows correct order (H1 → H2 → H3)
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I audit the heading structure
Then there should be exactly one H1 on the page
And H2 headings should follow H1
And no heading levels should be skipped
```

### Scenario 10.3: Interactive elements are keyboard accessible
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I navigate using the Tab key
Then focus should move through: navigation links → hero CTAs → feature CTAs → FAQ items → footer links
And all interactive elements should have a visible focus indicator
```

### Scenario 10.4: FAQ accordion is accessible via keyboard
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I navigate to the FAQ section using Tab key
Then pressing Enter or Space on a FAQ item should expand/collapse it
And the expanded/collapsed state should be announced via aria-expanded
```

### Scenario 10.5: Colour contrast meets WCAG AA minimum (4.5:1)
```gherkin
Given the Adobe LLM Optimizer landing page is open
When I run an automated contrast check on all text elements
Then no text element should fail WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text)
```

---

## Feature: Performance

### Scenario 11.1: Page load time is within acceptable threshold
```gherkin
Given the Adobe LLM Optimizer landing page is open in a clean browser session
When the page reaches load event
Then Time to First Byte (TTFB) should be < 600ms
And First Contentful Paint (FCP) should be < 2.5s
And Largest Contentful Paint (LCP) should be < 4s
```

### Scenario 11.2: No console errors on page load
```gherkin
Given the Adobe LLM Optimizer landing page is open
When the page reaches network idle state
Then the browser console should have zero error-level messages
And no 4xx or 5xx resource requests should occur
```

### Scenario 11.3: All images load without broken image icons
```gherkin
Given the Adobe LLM Optimizer landing page is open
When all page resources finish loading
Then no img element should display a broken image icon
And all image network requests should return HTTP 200
```

---

## Feature: Cross-Browser Compatibility

### Scenario 12.1: Page renders correctly in Firefox
```gherkin
Given the page is opened in Firefox 127+ at 1920x1080
When the page loads
Then the hero heading, all feature blocks, FAQ, and footer should be visible
And no CSS layout issues should occur
```

### Scenario 12.2: Page renders correctly in Safari (WebKit)
```gherkin
Given the page is opened in Safari/WebKit at 1920x1080
When the page loads
Then the hero heading, all feature blocks, FAQ, and footer should be visible
And the countdown timer should display correctly
```

### Scenario 12.3: Page renders correctly in Microsoft Edge
```gherkin
Given the page is opened in Edge (Chromium) at 1920x1080
When the page loads
Then all sections and interactive elements should function identically to Chrome
```

### Scenario 12.4: FAQ accordion functions in all browsers
```gherkin
Given the page is opened in Chrome, Firefox, Safari, and Edge
When I click a FAQ item in each browser
Then the accordion should expand and collapse correctly in all four browsers
```

---

## Summary

| Group | Tag | Scenarios | Priority |
|---|---|---|---|
| 1 — Global Navigation | @ui @nav | 8 | High |
| 2 — Hero Section | @ui @hero | 7 | Critical |
| 3 — Feature Block A | @ui @feature | 5 | High |
| 4 — Feature Block B | @ui @feature | 5 | High |
| 5 — Feature Block C | @ui @feature | 5 | High |
| 6 — FAQ Accordion | @ui @accordion | 6 | High |
| 7 — Contact / CTA Banner | @ui @cta | 3 | Medium |
| 8 — Global Footer | @ui @footer | 6 | Medium |
| 9 — Responsive Layout | @responsive | 6 | High |
| 10 — Accessibility | @a11y | 5 | Medium |
| 11 — Performance | @perf | 3 | Medium |
| 12 — Cross-Browser | @compat | 4 | High |
| **Total** | | **63** | |
