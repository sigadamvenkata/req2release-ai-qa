# Test Cases — MWPW-199796: YouTube Gallery Block

## Feature: YouTube Gallery Block

---

### Scenario Group 1 — Page Load & Heading

#### @smoke
**Scenario: Page loads successfully with HTTP 200**
```gherkin
Given I navigate to the YouTube Gallery page
Then the page returns HTTP status 200
And the page title is not empty
```

#### @smoke @ui
**Scenario: Gallery block has a valid visible heading**
```gherkin
Given I navigate to the YouTube Gallery page
Then a gallery block heading is visible on the page
And the heading text is not empty
```

---

### Scenario Group 2 — Grid Layout & Card Structure

#### @smoke @ui
**Scenario: Gallery renders at least one card in a grid layout**
```gherkin
Given I navigate to the YouTube Gallery page
Then the gallery grid container is visible
And at least 1 gallery card is present within the grid
```

#### @ui
**Scenario: Cards are arranged in a grid with consistent alignment**
```gherkin
Given I navigate to the YouTube Gallery page
When I inspect the card layout
Then all cards share the same column width
And cards are vertically aligned without overflow
```

---

### Scenario Group 3 — Card Metadata

#### @smoke @ui
**Scenario: Each card displays a thumbnail image**
```gherkin
Given I navigate to the YouTube Gallery page
When I inspect the first gallery card
Then a thumbnail image element is visible within the card
And the image src attribute is not empty
```

#### @ui
**Scenario: Each card has a unique ID attribute**
```gherkin
Given I navigate to the YouTube Gallery page
When I collect all gallery card IDs
Then every card ID is non-empty
And all card IDs are unique across the gallery
```

#### @ui
**Scenario: Each card displays label text**
```gherkin
Given I navigate to the YouTube Gallery page
When I inspect the first gallery card
Then a label text element is visible within the card
And the label text is not empty
```

#### @ui
**Scenario: Each card displays a Free tag**
```gherkin
Given I navigate to the YouTube Gallery page
When I inspect the first gallery card
Then a tag element is visible within the card
And the tag text equals "Free"
```

---

### Scenario Group 4 — Hover Behaviour (Video Playback)

#### @smoke @functional
**Scenario: Hovering over a card starts inline video playback**
```gherkin
Given I navigate to the YouTube Gallery page
And the first gallery card is visible
When I hover over the first gallery card
Then a video element becomes visible within the card
And the video is in a playing state (not paused)
```

#### @functional
**Scenario: Video stops or hides when hover is removed**
```gherkin
Given I navigate to the YouTube Gallery page
And I am hovering over the first gallery card
And the card video is playing
When I move the mouse away from the card
Then the video returns to a paused or hidden state
```

#### @functional
**Scenario: Hovering over a second card plays its own video**
```gherkin
Given the gallery has at least 2 cards visible
When I hover over the second gallery card
Then the second card video becomes visible and plays
And the first card video is not playing
```

---

### Scenario Group 5 — No Click Action / Navigation

#### @smoke @functional
**Scenario: Clicking a card does not navigate away from the page**
```gherkin
Given I navigate to the YouTube Gallery page
And the current URL is recorded
When I click on the first gallery card
Then the current URL has not changed
And the page content remains the gallery page
```

#### @functional
**Scenario: Card has no anchor tag linking to an external page**
```gherkin
Given I navigate to the YouTube Gallery page
When I inspect the first gallery card element
Then the card root element is not an anchor tag
And no child anchor navigates outside the current page on click
```

---

### Scenario Group 6 — Cross-Browser Compatibility

#### @smoke @compat
**Scenario: Gallery loads and heading is visible on Firefox**
```gherkin
Given I open the YouTube Gallery page in Firefox
Then the gallery heading is visible
And at least 1 card is present
```

#### @smoke @compat
**Scenario: Gallery loads and heading is visible on WebKit (Safari)**
```gherkin
Given I open the YouTube Gallery page in WebKit
Then the gallery heading is visible
And at least 1 card is present
```

#### @compat
**Scenario: Hover video playback works on Firefox**
```gherkin
Given I open the YouTube Gallery page in Firefox
When I hover over the first gallery card
Then the video element is visible and in a playing state
```

---

### Scenario Group 7 — Mobile Compatibility (Viewport Simulation)

#### @smoke @mobile
**Scenario: Gallery renders correctly on mobile portrait viewport (375x812)**
```gherkin
Given the viewport is set to 375 x 812 (portrait)
And I navigate to the YouTube Gallery page
Then the gallery grid is visible
And at least 1 card is visible without horizontal overflow
```

#### @mobile
**Scenario: Gallery renders correctly on mobile landscape viewport (812x375)**
```gherkin
Given the viewport is set to 812 x 375 (landscape)
And I navigate to the YouTube Gallery page
Then the gallery grid is visible
And at least 1 card is visible without horizontal overflow
```

#### @mobile
**Scenario: No horizontal scrollbar appears on mobile portrait viewport**
```gherkin
Given the viewport is set to 375 x 812 (portrait)
And I navigate to the YouTube Gallery page
Then the page body scroll width equals the viewport width
And no horizontal scrollbar is present
```

---

### Scenario Group 8 — Page-Level Layout

#### @ui
**Scenario: Page has no layout overflow on desktop**
```gherkin
Given the viewport is set to 1440 x 900
And I navigate to the YouTube Gallery page
Then the page renders without a horizontal scrollbar
```

#### @ui
**Scenario: Page has a non-empty meta description**
```gherkin
Given I navigate to the YouTube Gallery page
Then the meta description tag is present
And the meta description content is not empty
```

---

### Scenario Group 9 — Stock API Integration

#### @smoke @integration
**Scenario: Stock API is called when the gallery page loads**
```gherkin
Given I am monitoring network requests
When I navigate to the YouTube Gallery page
Then at least one network request is made to the Stock API endpoint
And the request receives an HTTP 2xx response
```

#### @integration
**Scenario: Stock API response contains valid card data**
```gherkin
Given I intercept the Stock API response on page load
When the gallery page finishes loading
Then the API response body is not empty
And the response contains card entries with id, label, and image fields
```

#### @integration
**Scenario: Gallery cards are populated from Stock API data**
```gherkin
Given the Stock API returns a successful response with card data
When the gallery page finishes rendering
Then the number of visible gallery cards matches the count returned by the API
And each card's ID matches a corresponding entry in the API response
```

#### @integration
**Scenario: Stage environment calls the stage Stock API endpoint**
```gherkin
Given the test environment is set to "stage"
And I am monitoring network requests
When I navigate to the YouTube Gallery stage page
Then all Stock API requests target the stage endpoint domain
And no requests are made to the production Stock API domain
```

#### @integration
**Scenario: Production environment calls the production Stock API endpoint**
```gherkin
Given the test environment is set to "production"
And I am monitoring network requests
When I navigate to the YouTube Gallery production page
Then all Stock API requests target the production endpoint domain
And no requests are made to the stage Stock API domain
```

#### @integration
**Scenario: Gallery handles Stock API error response gracefully**
```gherkin
Given the Stock API is mocked to return an HTTP 500 error
When I navigate to the YouTube Gallery page
Then no unhandled JavaScript errors are thrown
And the gallery block does not crash or display a broken layout
```

#### @integration
**Scenario: Stock API request includes required headers or parameters**
```gherkin
Given I intercept outgoing requests to the Stock API
When the gallery page loads
Then each Stock API request includes the expected query parameters or headers
And the request method is GET
```
