# SpiritTree Marketplace Rebuild Spec

## OBJECTIVE
Rebuild the entire SpiritTree Marketplace site to match shopclawmart.com's design system exactly, adapted for SpiritTree's products.

## REFERENCE: ClawMart Design System (extracted from live site HTML)

### Colors (from Tailwind config)
- `bg-sand-50` = warm off-white background (~#faf8f5)
- `bg-white` = card/section backgrounds
- `text-ink-900` = primary text (dark, ~#1a1a2e)
- `text-ink-700` = secondary text
- `text-ink-600` = muted text
- `text-ink-500` = lighter muted
- `text-tide-600` = accent teal (~#0d9488)
- `text-tide-700` = accent hover
- `border-ink-900/5` = subtle borders
- `border-ink-900/10` = card borders
- `bg-tide-500/10` = accent light bg
- `bg-tide-600` = accent buttons
- `bg-ink-900` = dark buttons/CTA band

### Layout Patterns
- Max width: `max-w-6xl` (1152px)
- Padding: `px-6`
- Card grid: 3 columns on desktop, 2 on tablet, 1 on mobile
- Section spacing: `py-16`

### Nav (LIGHT - sticky)
```html
<header class="sticky top-0 z-50 border-b border-ink-900/5 bg-sand-50/80 backdrop-blur-lg">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6 sm:py-4">
    <a class="font-display text-xl font-semibold text-ink-900" href="/">Brand Name</a>
    <nav class="hidden items-center gap-6 text-sm font-medium text-ink-700 md:flex">
      <a href="/browse">Browse</a>
      <a href="/about">About</a>
      <a href="/blog">Blog</a>
      <a class="rounded-full border border-ink-900/15 px-3 py-1.5 text-sm font-semibold text-ink-900" href="/login">Login / Sign Up</a>
    </nav>
    <!-- hamburger for mobile -->
  </div>
</header>
```

### Product Card Pattern
```html
<article class="group flex flex-col rounded-2xl border border-ink-900/5 bg-white p-5 shadow-card transition hover:shadow-card-hover">
  <div class="flex items-start justify-between gap-3">
    <div class="flex items-center gap-3">
      <div class="card-icon">🤖</div> <!-- or letter avatar -->
      <div>
        <h3 class="font-display text-lg font-semibold text-ink-900">Product Name</h3>
        <p class="text-sm text-ink-600">Category</p>
      </div>
    </div>
    <span class="rounded-full bg-tide-500/10 px-2.5 py-1 text-sm font-semibold text-tide-700">$99</span>
  </div>
  <p class="mt-4 text-sm leading-relaxed text-ink-600 flex-1">Description</p>
  <div class="mt-4 flex flex-wrap gap-1.5">
    <span class="rounded-md bg-sand-100 px-2 py-0.5 text-xs font-medium text-ink-700">Category</span>
  </div>
  <div class="mt-5 flex items-center justify-between border-t border-ink-900/5 pt-4">
    <span class="text-sm text-ink-600">SpiritTree</span>
    <a class="rounded-lg bg-tide-600 px-3 py-1.5 text-sm font-semibold text-white transition hover:bg-tide-700" href="#">Buy</a>
  </div>
</article>
```

### Footer (LIGHT)
```html
<footer class="border-t border-ink-900/5 bg-white">
  <div class="mx-auto max-w-6xl px-6 py-10">
    <div class="grid gap-10 sm:grid-cols-2">
      <div>
        <p class="text-sm font-semibold text-ink-900">SpiritTree</p>
        <nav class="mt-3 flex flex-col gap-2">
          <a class="text-sm text-ink-600 hover:text-ink-900" href="#">Link</a>
        </nav>
      </div>
      <div>
        <p class="text-sm font-semibold text-ink-900">Products</p>
        <nav class="mt-3 columns-2 gap-x-8">
          <a class="mb-2 block text-sm text-ink-600 hover:text-ink-900" href="#">Link</a>
        </nav>
      </div>
    </div>
    <div class="mt-8 border-t border-ink-900/5 pt-6">
      <p class="text-sm text-ink-500">© 2026 Nrvana LLC</p>
    </div>
  </div>
</footer>
```

### Homepage Sections (in order, from ClawMart)
1. Hero: Title + subtitle + 2 CTA buttons (Browse, Sell Your Own)
2. Three-stat strip: Pre-built / Battle-tested / Plug & play
3. Most Popular products grid (6 cards, 3-col)
4. Newsletter section (email input + subscribe)
5. Featured creators grid
6. How it works (1-2-3 steps)
7. Creator API section (split: text left, code block right)
8. Dark CTA band ("Ready to build?" - bg-ink-900)
9. Light footer

### About Page Pattern
- Sections in white rounded cards with shadow
- Content sections: About, Two product types (grid), How it works (numbered list), For creators (stats grid), Why this exists

### Blog Page Pattern
- Title + subtitle
- Grid of blog post cards with date, read time, title, description, "Read article →" link

### Login Page Pattern
- Centered card with title "Account access"
- Subtitle: "One account for buyers and creators"
- Email input, password input, forgot password link
- "Looking for products? Browse marketplace" link at bottom

## LANDON'S REQUIREMENTS

### 1. REMOVE ALL DARK BACKGROUNDS
- Nav: light (sand-50/80 with backdrop-blur)
- Footer: white bg
- Page headers: white/sand bg (NOT dark navy)
- Mobile menu: light bg

### 2. GLOBAL BORDER-RADIUS: 4px
**CRITICAL: border-radius: 4px on EVERYTHING**
- All buttons
- All cards
- All pills/badges
- All inputs
- All icons
- No rounded-full, no rounded-2xl, no rounded-xl
- ONLY 4px everywhere

### 3. FIX FILTER TABS (browse.html)
The filter pills (All, Consulting, Digital, Security, Tools, Free) need working JavaScript:
```javascript
document.querySelectorAll('.filter-pill').forEach(pill => {
  pill.addEventListener('click', function() {
    // Remove active from all
    document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
    this.classList.add('active');
    
    const filter = this.textContent.trim().toLowerCase();
    document.querySelectorAll('.browse-section').forEach(section => {
      if (filter === 'all') {
        section.style.display = '';
      } else {
        const sectionCategory = section.dataset.category;
        section.style.display = sectionCategory === filter ? '' : 'none';
      }
    });
  });
});
```
Add data-category attributes to each section div.

### 4. OPTIMIZE CODE
- Clean, consistent CSS
- All nav links working
- Responsive design
- No redundant code

### 5. ACCOUNT LOGIN PAGE
- Create login.html
- Simple form: email + password
- "Forgot password?" link
- Link back to browse
- Add "Login / Sign Up" to nav on all pages

## SPIRITTREE PRODUCTS (keep all existing)

### Consulting
- Agent Blueprint Roadmap — $497 (link: https://buy.stripe.com/00wfZa2qE1AZ09F70z2Nq01)
- Roadmap + Build — $997 (link: https://buy.stripe.com/9B63co8P2a7v3lRfx52Nq02)
- Full Operations — $1,997 (link: https://buy.stripe.com/6oU00c0iw2F3aOj2Kj2Nq03)

### Digital Products
- Agent Blueprint DIY Kit — $49 (link: https://buy.stripe.com/7sY00c2qE5Rf1dJacL2Nq07)
- Content Pipeline Templates — $79 (link: https://buy.stripe.com/6oUbIU2qEa7vf4zet12Nq0a)
- SafeSpace Civic Toolkit — $99 (link: https://buy.stripe.com/aFa4gsc1eenL6y3et12Nq08)
- AI Cost Optimizer — $149 (link: https://buy.stripe.com/eVqeV63uI7ZnaOj5Wv2Nq09)
- CEO Operations Stack — $149
- SafeSpace Template — $99
- Content Pipeline System — $79
- DIY Setup Guide — $49

### Security
- OpenClaw Hardening Guide — $49
- Done-For-You Security Audit — $297

### Bundle
- OpenClaw Mastery Bundle — $29

### Free Tools
- SkillScan — Free
- SafeSpace — Free
- MycoMaps — Free

## FILES TO UPDATE
1. index.html — full homepage rebuild matching ClawMart sections
2. browse.html — all products with WORKING filter tabs
3. consulting.html — consulting page
4. blog.html — blog listing
5. tools.html — tools page
6. about.html — about page
7. All files in products/ directory
8. CREATE: login.html

## CSS APPROACH
Since this is static HTML (GitHub Pages), use inline `<style>` in each file. Define a shared CSS design system at the top of each file matching ClawMart's patterns but with 4px border-radius override.

## IMPLEMENTATION NOTES
- Use system sans-serif font stack (like ClawMart)
- No external CSS frameworks needed — vanilla CSS
- Keep all existing Stripe payment links
- Keep CNAME file untouched
- Mobile hamburger menu must work
- All internal links must resolve to actual files
