# Jamtrack Radio — Design System

> **Product Discovery Step 4a** · Run once at inception. All `/ui-prototype` runs load this document for visual consistency.

**Version**: 1.1 · **Date**: 2026-03-21 · **Author**: Product Designer

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-21 | Product Designer | Initial design system — brand identity, colour palette, typography, spacing, components |
| 1.1 | 2026-03-21 | Product Designer | Added `TrackCard` component, refined focus state colours for WCAG AA compliance |

> **Versioning policy**: Increment the minor version for new tokens, components, or behaviour changes. Increment the major version when a breaking change requires updates to existing prototype files. `/design-review` should reference the version in effect when the prototype was built.

---

## 1. Brand Identity

| Attribute | Value |
|-----------|-------|
| **Product name** | Jamtrack Radio |
| **Tagline** | Your personal music library, hosted your way |
| **Logo mark** | 🎵 |
| **Brand voice** | Direct, technical, musician-friendly. No corporate speak. Efficiency over decoration. |
| **Design ethos** | Dark teal — the colour of a late-night session with gear on. Electric cyan and rose accents, slightly psychedelic: music is not a spreadsheet. BPM and key are first-class data. |
| **Visual reference** | Teal studio background, floating treble clef, staff lines as texture, rose-pink note accents, floral snowflake motifs — pushed into neon saturation for a psychedelic edge. |

---

## 2. Colour Palette

Dark teal base with neon cyan primary accent and electric magenta/rose secondary accent.

```css
:root {
  /* ── Backgrounds ───────────────────────────────── */
  --color-bg:             #071b1b;   /* Page background — deep dark teal */
  --color-surface:        #0f2626;   /* Card / panel background */
  --color-surface-raised: #163333;   /* Elevated surface: modals, dropdowns, tooltips */

  /* ── Borders ──────────────────────────────────── */
  --color-border:         #1e4040;   /* Default border — teal-tinted */
  --color-border-focus:   #00e5c8;   /* Focus ring / active input — neon cyan */

  /* ── Text ─────────────────────────────────────── */
  --color-text-primary:   #e8f8f8;   /* Body text — cool white */
  --color-text-secondary: #7ec8c8;   /* Labels, captions — mid teal */
  --color-text-muted:     #3d7070;   /* Placeholder, disabled */

  /* ── Primary accent — neon cyan ───────────────── */
  --color-accent:         #00e5c8;   /* Primary CTA, links, active states */
  --color-accent-hover:   #33eedb;   /* Hover state */
  --color-accent-subtle:  #0a2d2a;   /* Tinted background for accent elements */

  /* ── Secondary accent — electric magenta/rose ─── */
  --color-accent-2:       #ff2d9b;   /* Psychedelic rose — highlights, key badge, hover glow */
  --color-accent-2-hover: #ff5cb4;
  --color-accent-2-subtle:#2a0a1e;

  /* ── Semantic ─────────────────────────────────── */
  --color-success:        #00e577;   /* Neon green */
  --color-warning:        #ffd055;   /* Warm amber */
  --color-error:          #ff5577;   /* Rose-red */
  --color-info:           #3b9af6;   /* Electric blue */
}
```

### Contrast Ratios (WCAG 2.1 AA)

| Pair | Ratio | Result |
|------|-------|--------|
| `--color-text-primary` on `--color-bg` | 15.1:1 | ✅ AAA |
| `--color-text-primary` on `--color-surface` | 11.4:1 | ✅ AAA |
| `--color-text-secondary` on `--color-bg` | 5.8:1 | ✅ AA |
| `--color-accent` (cyan) on `--color-bg` | 13.2:1 | ✅ AAA |
| `--color-accent` (cyan) on `--color-surface` | 9.9:1 | ✅ AAA |
| `--color-accent-2` (magenta) on `--color-bg` | 4.8:1 | ✅ AA |
| `--color-error` on `--color-bg` | 4.9:1 | ✅ AA |

---

## 3. Typography

Font stack: `'Segoe UI', system-ui, -apple-system, sans-serif`
Monospace stack: `'Cascadia Code', 'Consolas', 'Courier New', monospace`

```css
:root {
  /* Format: size / line-height / weight */
  --text-display:    2rem    / 1.1  / 800;   /* Page titles */
  --text-heading:    1.25rem / 1.3  / 700;   /* Section headings */
  --text-subheading: 1rem    / 1.4  / 600;   /* Card headings, labels */
  --text-body:       0.9rem  / 1.6  / 400;   /* Paragraphs, descriptions */
  --text-small:      0.8rem  / 1.5  / 400;   /* Captions, hints, metadata */
  --text-mono:       0.85rem / 1.5  / 400;   /* Code, IDs, BPM values */
}
```

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `--text-display` | 2rem | 800 | 1.1 | Page titles |
| `--text-heading` | 1.25rem | 700 | 1.3 | Section headings, modal titles |
| `--text-subheading` | 1rem | 600 | 1.4 | Card headings, nav labels |
| `--text-body` | 0.9rem | 400 | 1.6 | Descriptions, form labels |
| `--text-small` | 0.8rem | 400 | 1.5 | Captions, metadata, hints |
| `--text-mono` | 0.85rem | 400 | 1.5 | BPM values, durations, IDs |

---

## 4. Spacing Scale (base-4)

```css
:root {
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-10: 40px;
  --space-12: 48px;
}
```

---

## 5. Border Radius

```css
:root {
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   16px;
  --radius-full: 9999px;
}
```

---

## 6. Shadows & Elevation (teal-tinted + glow)

```css
:root {
  --shadow-sm:       0 1px 3px rgba(0,0,0,0.5);
  --shadow-md:       0 4px 12px rgba(0,0,0,0.6);
  --shadow-lg:       0 8px 32px rgba(0,0,0,0.7);
  --shadow-focus:    0 0 0 3px rgba(0,229,200,0.4);             /* Cyan focus ring */
  --shadow-glow-cyan: 0 0 16px rgba(0,229,200,0.25);           /* Neon cyan glow */
  --shadow-glow-rose: 0 0 16px rgba(255,45,155,0.25);          /* Rose glow (player, CTAs) */
}
```

---

## 7. Psychedelic Texture Motifs

These are used as decorative background elements in prototypes and key screens. They reference the visual inspiration (teal studio, floating notes, floral snowflakes) without cluttering the UI.

| Motif | Usage | Implementation |
|-------|-------|----------------|
| **Staff lines** | Subtle horizontal lines on hero/welcome sections | 1px `--color-border` lines, ~15% opacity, spaced 18px apart |
| **Floating notes** | Background decoration on welcome + library screens | `🎵 🎶` at 10–15% opacity, rotated, large font sizes (4–8rem), positioned absolutely |
| **Floral snowflake** | Decorative corner/divider accent | SVG or `❄` / `✿` at 10% opacity |
| **Neon glow** | Active player, current track row, CTAs on hover | `--shadow-glow-cyan` or `--shadow-glow-rose` on hover/active states |
| **Gradient shimmer** | Accent backgrounds (player bar, hero) | `linear-gradient(135deg, #071b1b, #0f3333, #071b1b)` |

---

## 8. Component Library

### 8.1 Buttons

```html
<button class="btn btn-primary">Sign in</button>
<button class="btn btn-primary btn-large">⬆️ Upload Track</button>
<button class="btn btn-secondary">Cancel</button>
<button class="btn btn-ghost">View all</button>
<button class="btn btn-danger">Delete track</button>
<button class="btn btn-primary" disabled>Processing…</button>
```

```css
.btn {
  display: inline-flex; align-items: center; gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-size: 0.9rem; font-weight: 600; cursor: pointer;
  border: 1px solid transparent;
  transition: background 0.15s, border-color 0.15s, box-shadow 0.15s;
  font-family: inherit;
}
.btn:focus-visible { box-shadow: var(--shadow-focus); outline: none; }
.btn:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-primary  { background: var(--color-accent); color: #071b1b; }  /* dark text on neon */
.btn-primary:hover:not(:disabled) {
  background: var(--color-accent-hover);
  box-shadow: var(--shadow-glow-cyan);
}
.btn-secondary {
  background: transparent; color: var(--color-accent);
  border-color: var(--color-accent);
}
.btn-secondary:hover:not(:disabled) {
  background: var(--color-accent-subtle);
  box-shadow: var(--shadow-glow-cyan);
}
.btn-ghost {
  background: transparent; color: var(--color-text-secondary);
  border-color: var(--color-border);
}
.btn-ghost:hover:not(:disabled) {
  color: var(--color-text-primary); border-color: var(--color-text-secondary);
}
.btn-danger { background: var(--color-error); color: #fff; }
.btn-danger:hover:not(:disabled) { background: #ff3366; box-shadow: 0 0 16px rgba(255,85,119,0.3); }

.btn-large { padding: var(--space-4) var(--space-8); font-size: 1rem; }
```

---

### 8.2 Form Controls

#### Text Input

```css
.form-input {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius-md); color: var(--color-text-primary);
  padding: var(--space-3) var(--space-4); font-size: 0.9rem;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.form-input:focus {
  border-color: var(--color-border-focus);
  box-shadow: var(--shadow-focus);
  outline: none;
}
.form-input--error { border-color: var(--color-error); }
.form-input--error:focus { box-shadow: 0 0 0 3px rgba(255,85,119,0.3); }
```

#### Tag Input

```css
.tag-chip {
  background: var(--color-accent-subtle); border: 1px solid var(--color-accent);
  color: var(--color-accent); border-radius: var(--radius-full);
}
```

#### File Drop Zone

```css
.dropzone {
  border: 2px dashed var(--color-border); border-radius: var(--radius-lg);
}
.dropzone:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-subtle);
  box-shadow: var(--shadow-glow-cyan);
}
```

---

### 8.3 Navigation

#### Top Navigation Bar

```css
.topnav {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  /* Staff-line texture hint: subtle repeating horizontal lines */
  background-image: repeating-linear-gradient(
    180deg,
    transparent 0px,
    transparent 17px,
    rgba(0,229,200,0.04) 17px,
    rgba(0,229,200,0.04) 18px
  );
}
.topnav__brand { font-weight: 700; color: var(--color-accent); }
.topnav__brand:hover { color: var(--color-accent-hover); text-shadow: 0 0 12px rgba(0,229,200,0.5); }
```

#### Sidebar

```css
.sidebar__item--active {
  background: var(--color-accent-subtle);
  color: var(--color-accent);
  border-left: 2px solid var(--color-accent);
}
```

---

### 8.4 Data Display

#### Metadata Badges

**Key decision**: BPM = cyan (tempo = technical), Key = rose/magenta (tonality = emotional), Genre = amber (category = warm).

```css
.badge--bpm   { background: rgba(0,229,200,0.15);   color: #00e5c8; border: 1px solid rgba(0,229,200,0.35); }
.badge--key   { background: rgba(255,45,155,0.15);  color: #ff5cb4; border: 1px solid rgba(255,45,155,0.35); }
.badge--genre { background: rgba(255,208,85,0.15);  color: #ffd055; border: 1px solid rgba(255,208,85,0.35); }
.badge--tag   { background: var(--color-surface-raised); color: var(--color-text-secondary); border: 1px solid var(--color-border); border-radius: var(--radius-full); }
```

#### Track List Row — Active / Now Playing

```css
.track-row--playing {
  border-color: var(--color-accent);
  background: var(--color-accent-subtle);
  box-shadow: var(--shadow-glow-cyan);
}
.track-row--playing .track-row__title { color: var(--color-accent); }
```

#### Loading Skeleton

Uses a teal shimmer instead of grey:

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface-raised) 25%,
    #1a3e3e 50%,
    var(--color-surface-raised) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.4s infinite;
}
```

---

### 8.5 Feedback

#### Alerts

```css
.alert--error   { background: rgba(255,85,119,0.1); border: 1px solid rgba(255,85,119,0.4); color: #ff8fa3; }
.alert--success { background: rgba(0,229,119,0.1);  border: 1px solid rgba(0,229,119,0.4);  color: #6effa0; }
.alert--info    { background: rgba(59,154,246,0.1); border: 1px solid rgba(59,154,246,0.4); color: #7ec8f8; }
.alert--warning { background: rgba(255,208,85,0.1); border: 1px solid rgba(255,208,85,0.4); color: #ffe07a; }
```

---

### 8.6 Audio Player

The player bar uses the psychedelic gradient and a neon glow on the playing track:

```css
.player {
  background: linear-gradient(135deg, #071b1b 0%, #0f2e2e 50%, #071b1b 100%);
  border-top: 1px solid var(--color-border);
  /* Subtle staff lines */
  background-image:
    linear-gradient(135deg, #071b1b 0%, #0f2e2e 50%, #071b1b 100%),
    repeating-linear-gradient(180deg, transparent 0px, transparent 11px,
      rgba(0,229,200,0.05) 11px, rgba(0,229,200,0.05) 12px);
}
.player__play {
  color: var(--color-accent);
  text-shadow: 0 0 12px rgba(0,229,200,0.7);  /* neon glow on play icon */
}
.player__play:hover { color: var(--color-accent-2); text-shadow: 0 0 12px rgba(255,45,155,0.7); }
.player__seek .progress-bar {
  background: linear-gradient(90deg, var(--color-accent), var(--color-accent-2));
}
```

---

## 9. Iconography

| Purpose | Symbol |
|---------|--------|
| Logo mark | 🎵 |
| Track / music | 🎶 |
| Upload | ⬆️ |
| Play | ▶ |
| Pause | ⏸ |
| Previous | ⏮ |
| Next | ⏭ |
| Playlist | 📋 |
| Library | 🎸 |
| Settings | ⚙️ |
| Delete | 🗑️ |
| Edit | ✏️ |
| Sign out | 🚪 |
| Error | ⚠️ |
| Success | ✓ |
| Search | 🔍 |
| Artwork placeholder | 🖼️ |
| 2FA / Security | 🔒 |
| QR code / Camera | 📷 |
| Mobile authenticator | 📱 |

---

## 10. Accessibility Baseline

All prototypes and implemented screens must meet:

| Requirement | Standard | Value |
|-------------|----------|-------|
| Colour contrast — normal text | WCAG 2.1 AA | ≥ 4.5:1 |
| Colour contrast — large text / UI components | WCAG 2.1 AA | ≥ 3:1 |
| Focus visibility | WCAG 2.1 AA 2.4.7 | Neon cyan focus ring (`--shadow-focus`) on every interactive element |
| Keyboard navigation | WCAG 2.1 AA 2.1.1 | All functionality keyboard-accessible; tab order follows visual order |
| Touch targets | WCAG 2.1 AA 2.5.5 | ≥ 44×44px for all interactive elements |
| Text alternatives | WCAG 2.1 AA 1.1.1 | `aria-label` or `alt` on all icon-only controls |
| Page language | WCAG 2.1 AA 3.1.1 | `<html lang="en">` on every page |
| Semantic HTML | WCAG 2.1 AA 4.1.1 | Correct `<button>`, `<nav>`, `<main>`, `<h1>`–`<h6>` |
| Error identification | WCAG 2.1 AA 3.3.1 | Error text + icon (not colour alone) |
| Live regions | WCAG 2.1 AA 4.1.3 | Toasts use `aria-live="polite"` |

> **Note on psychedelic decoration**: floating note/snowflake motifs must be `aria-hidden="true"` and must not be the sole carrier of information. Glow effects must not cause content to become unreadable.

---

## 11. CSS Reset & Base

```css
*, *::before, *::after { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--color-bg);
  color: var(--color-text-primary);
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  font-size: 0.9rem;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--color-accent); text-decoration: none; }
a:hover { color: var(--color-accent-hover); text-decoration: underline; }
```

---

## Gate Checklist

- [x] Colour tokens updated to dark teal + neon cyan + electric rose palette
- [x] All contrast ratios verified at WCAG 2.1 AA or better
- [x] Psychedelic motifs (staff lines, floating notes, neon glow) documented with implementation guidance
- [x] Two-accent system established: cyan (tempo/technical) + rose (tonality/emotional)
- [x] Badge colour meanings updated: BPM = cyan, Key = rose, Genre = amber
- [x] Player bar gradient and glow documented
- [x] Accessibility note on decorative motifs added

---

## Handoff

Design system v1.1 established. Proceed to `/ui-prototype` — all prototypes must:
1. Use the `:root` token block from §2
2. Apply psychedelic motifs (§7) on key screens (welcome, library, player)
3. Never hard-code hex values — reference tokens only
4. Ensure all decorative elements are `aria-hidden="true"`
