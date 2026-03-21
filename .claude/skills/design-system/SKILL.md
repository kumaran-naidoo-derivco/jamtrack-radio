---
name: design-system
description: Establishes and documents the Jamtrack Radio visual design language — colour palette, typography, spacing, component library, and dark theme conventions. Run once during Product Discovery (Step 4a). All subsequent /ui-prototype runs load this document for consistency.
disable-model-invocation: true
argument-hint: [optional: component or section to update]
---

You are acting as the **Product Designer** establishing the Jamtrack Radio design system. This is run **once** during Product Discovery to define the visual language that all future UI prototypes must follow. If called with an argument, update or extend the relevant section of the existing design system.

---

## What to Produce

### 1. Design System Document

Save to `docs/design-system/jamtrack-radio-design-system.md`.

The document must cover all sections below. Be specific — every value must be a concrete token (hex code, pixel value, rem value), not a vague description.

---

#### 1.1 Brand Identity

- **Product name**: Jamtrack Radio
- **Tagline**: Your personal music library, hosted your way
- **Brand voice**: Direct, technical, musician-friendly. No corporate speak. Efficiency over decoration.
- **Primary icon/emoji**: 🎵 (used as logo mark in prototypes)

---

#### 1.2 Colour Palette

Define tokens using CSS custom property naming. Include:

| Token | Role | Value |
|-------|------|-------|
| `--color-bg` | Page background | |
| `--color-surface` | Card / panel background | |
| `--color-surface-raised` | Elevated surface (modals, dropdowns) | |
| `--color-border` | Default border | |
| `--color-border-focus` | Focus ring / active input border | |
| `--color-text-primary` | Body text | |
| `--color-text-secondary` | Labels, captions | |
| `--color-text-muted` | Placeholder, disabled | |
| `--color-accent` | Primary CTA, links, active states | |
| `--color-accent-hover` | Hover state of accent | |
| `--color-accent-subtle` | Tinted background for accent elements | |
| `--color-success` | Success states, badges | |
| `--color-warning` | Warning states | |
| `--color-error` | Error states, destructive actions | |
| `--color-info` | Informational states | |

Use a dark-first palette. The background must be a deep near-black; the accent must be visible and accessible at AA contrast against both surface and background.

---

#### 1.3 Typography

| Token | Usage | Font | Size | Weight | Line height |
|-------|-------|------|------|--------|-------------|
| `--text-display` | Page titles | System UI | 2rem | 800 | 1.1 |
| `--text-heading` | Section headings | System UI | 1.25rem | 700 | 1.3 |
| `--text-subheading` | Card headings, labels | System UI | 1rem | 600 | 1.4 |
| `--text-body` | Paragraphs, descriptions | System UI | 0.9rem | 400 | 1.6 |
| `--text-small` | Captions, hints, metadata | System UI | 0.8rem | 400 | 1.5 |
| `--text-mono` | Code, IDs, technical values | Monospace | 0.85rem | 400 | 1.5 |

Font stack: `'Segoe UI', system-ui, -apple-system, sans-serif`

---

#### 1.4 Spacing Scale

Use a base-4 scale. Define tokens `--space-1` through `--space-12`.

| Token | Value | Common use |
|-------|-------|-----------|
| `--space-1` | 4px | Icon gap |
| `--space-2` | 8px | Input padding (vertical) |
| `--space-3` | 12px | Button padding (vertical), list item gap |
| `--space-4` | 16px | Card padding (small), form group gap |
| `--space-5` | 20px | Nav padding |
| `--space-6` | 24px | Card padding (standard), section gap |
| `--space-8` | 32px | Page horizontal padding |
| `--space-10` | 40px | Section gap (large) |
| `--space-12` | 48px | Hero padding |

---

#### 1.5 Border Radius

| Token | Value | Use |
|-------|-------|-----|
| `--radius-sm` | 4px | Tags, badges, small chips |
| `--radius-md` | 8px | Inputs, buttons, small cards |
| `--radius-lg` | 12px | Cards, panels |
| `--radius-xl` | 16px | Modal dialogs, large cards |
| `--radius-full` | 9999px | Pills, circular avatars |

---

#### 1.6 Component Library

Document the HTML + CSS for each component. Every component must include:
- Default state
- Hover / focus state
- Disabled state (where applicable)
- Error state (where applicable)

Components to document:

**Buttons**
- `btn-primary` — filled, accent colour, for primary CTAs
- `btn-secondary` — outlined, accent colour, for secondary actions
- `btn-ghost` — transparent with border, for tertiary actions
- `btn-danger` — red, for destructive actions
- Size variants: default, large (`btn-large`)

**Form Controls**
- Text input (default, focus, error, disabled)
- Select / dropdown
- Textarea
- Tag input (chips that can be added/removed)
- File picker / drop zone

**Navigation**
- Top navigation bar
- Sidebar navigation item (default, active, hover)
- Breadcrumbs

**Data Display**
- Track list row (artwork + title/artist + metadata badges + play button + actions)
- Metadata badge (BPM, key, genre — each with distinct colour)
- Tag pill (user-defined labels)
- Empty state (icon + heading + CTA)
- Loading skeleton (for track list rows)

**Feedback**
- Error message block (inline form error)
- Success toast
- Confirmation dialog (for destructive actions)
- Progress bar (for file upload)

**Audio Player**
- Play / pause button
- Waveform / progress bar (seek support)
- Volume control
- Track info strip (title, artist, BPM, key)

---

#### 1.7 Iconography

Use Unicode emoji as icon placeholders in HTML prototypes (no icon font dependency):

| Purpose | Emoji |
|---------|-------|
| Logo mark | 🎵 |
| Track / music | 🎶 |
| Upload | ⬆️ |
| Play | ▶ |
| Pause | ⏸ |
| Previous / Next | ⏮ ⏭ |
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

---

#### 1.8 Accessibility Baseline

All prototypes and implemented screens must meet:
- **WCAG 2.1 AA** colour contrast: 4.5:1 for normal text, 3:1 for large text and UI components
- **Focus visibility**: every interactive element must have a visible `:focus` style (not `outline: none` without replacement)
- **Keyboard navigation**: tab order must follow visual reading order
- **Touch targets**: minimum 44×44px for all interactive elements
- **Screen reader**: all images and icons used as controls must have `aria-label` or `alt` text

---

### 2. Component Showcase

Save to `docs/design-system/components.html`.

A single standalone HTML page that renders all components from section 1.6 in their various states. This is the living reference for developers — if a component looks right in this file, it's the source of truth.

Structure:
```html
<!-- Section per component, e.g.: -->
<section id="buttons">
  <h2>Buttons</h2>
  <!-- All button variants rendered side-by-side -->
</section>
```

---

## Output Format

```bash
mkdir -p docs/design-system
```

Files:
- `docs/design-system/jamtrack-radio-design-system.md` — the token and component documentation
- `docs/design-system/components.html` — live component showcase

---

## Gate

Design system is complete when:
- [ ] All colour tokens defined with hex values and contrast ratios checked
- [ ] All typography tokens defined with concrete size/weight/line-height values
- [ ] All spacing and radius tokens defined
- [ ] All components in section 1.6 documented with HTML + CSS
- [ ] Component showcase renders correctly in a browser
- [ ] Accessibility baseline documented

---

## Handoff

After the design system is established, proceed to:
- `/ui-prototype` — all prototypes must use the design system tokens and components from this document
