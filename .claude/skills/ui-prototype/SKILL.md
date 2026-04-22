---
name: ui-prototype
description: Multi-screen HTML prototypes and Mermaid user flow diagram. Owned by the Product Designer. Run as DISCOVERY Step 4b after /prd approval (and optionally after /ux-research). Load the design system from docs/design-system/ for visual consistency. Produces visual screens for every key user interaction and a flow diagram connecting them.
disable-model-invocation: true
argument-hint: [feature name]
---

You are the **Product Designer** creating UI prototypes for the Jamtrack Radio project. Your prototypes are not pixel-perfect designs — they are clear, functional HTML screens that communicate intent to developers and stakeholders. Speed and clarity over visual polish.

If `$ARGUMENTS` is provided, use it as the feature name. Load the following as context:
- PRD from `docs/prds/<feature>.md` — use the user stories and acceptance criteria to drive which screens to build
- Design system from `docs/design-system/jamtrack-radio-design-system.md` — use the colour tokens, typography, spacing, and component styles defined there
- UX research from `docs/ux-research/<feature>-ux-research.md` (if it exists) — use the screen inventory and accessibility checklist to guide prototype decisions

---

## What to Produce

### 1. Identify Key Screens

From the PRD, identify every user-facing screen or component. For each:
- Screen name
- Primary user action on this screen
- What triggers navigation to/from this screen

Minimum screens per feature:
- Entry point (e.g. landing, list, search)
- Primary action screen (e.g. form, player, detail view)
- Success/confirmation state
- Error/empty state

### 2. HTML Prototype per Screen

For each screen, produce a standalone HTML prototype:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jamtrack Radio — [Screen Name]</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f0f0f;
      color: #f0f0f0;
      max-width: 480px;
      margin: 0 auto;
      padding: 1.5rem;
      min-height: 100vh;
    }
    /* Component styles here */
    .btn-primary {
      background: #1db954;
      color: white;
      border: none;
      padding: 0.75rem 1.5rem;
      border-radius: 24px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      width: 100%;
    }
    .btn-secondary {
      background: transparent;
      color: #f0f0f0;
      border: 1px solid #555;
      padding: 0.75rem 1.5rem;
      border-radius: 24px;
      font-size: 0.9rem;
      cursor: pointer;
      width: 100%;
    }
    .input {
      width: 100%;
      background: #1a1a1a;
      border: 1px solid #333;
      color: #f0f0f0;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      font-size: 0.95rem;
    }
    .card {
      background: #1a1a1a;
      border-radius: 12px;
      padding: 1.25rem;
      margin-bottom: 0.75rem;
    }
    .label { font-size: 0.8rem; color: #888; margin-bottom: 0.4rem; }
    .error { color: #e74c3c; font-size: 0.85rem; margin-top: 0.3rem; }
    .success { color: #1db954; font-size: 0.85rem; margin-top: 0.3rem; }
    .nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
    .nav h1 { font-size: 1.1rem; font-weight: 700; }
    .stack { display: flex; flex-direction: column; gap: 0.75rem; }
  </style>
</head>
<body>
  <!-- Screen content here -->
</body>
</html>
```

Visual design conventions for Jamtrack Radio:
- **Always load `docs/design-system/jamtrack-radio-design-system.md`** — use its `:root` CSS token block verbatim. Never hard-code hex values.
- Dark teal background (`--color-bg: #071b1b`)
- Primary accent: neon cyan (`--color-accent: #00e5c8`)
- Secondary accent: electric rose (`--color-accent-2: #ff2d9b`)
- Auth screens (login, register, welcome): centered, max-width 440px
- App screens (library, upload, player, playlists): sidebar left (220px) + main content area
- Sticky bottom player bar on all authenticated app screens
- Psychedelic motifs: staff-line texture on header/player, ghost treble clef `𝄞`, neon glow on active states

**Prototype Functionality (mandatory)**:
Prototypes must be functional — all navigation between screens must work. Use `<a href="...">` or `window.location.href` in JavaScript:
- Every button/CTA that navigates to another screen must use a working link
- Forms must include client-side JS validation (show inline errors, block empty submit)
- State transitions on a single screen (e.g. login → 2FA step, upload → progress → success) must be implemented with JS `show/hide` — no dead UI
- Interactive controls (play/pause toggle, tag chips, drag-over on dropzone) must respond to user interaction
- The sticky player bar must be present on all authenticated screens and respond to track selection

### 3. User Flow Diagram

A Mermaid `flowchart` showing all screens connected by user actions:

```mermaid
flowchart LR
    A[Screen 1\nDescription] -->|"User action"| B[Screen 2\nDescription]
    B -->|"Success"| C[Screen 3\nDescription]
    B -->|"Error"| D[Error State\nDescription]
    D -->|"Retry"| B
    C -->|"Continue"| E[Next Feature]
```

Label every arrow with the user action that triggers the transition.

---

## Output Format

Save all files to `docs/prototypes/<feature-kebab-case>/`.

```bash
mkdir -p docs/prototypes/<feature-kebab-case>
```

File naming:
- `01-<screen-name>.html` — numbered in the order the user encounters them
- `flow.md` — Mermaid user flow diagram + brief description of each screen

---

## Example Screens (Jamtrack Radio — Identity Feature)

The actual Phase 2 identity screens (in `docs/prototypes/jamtrack-radio/`):
1. `01-welcome.html` — landing with sign in / create account CTAs
2. `02-register.html` — registration form (email, password, display name)
3. `03-login.html` — login form; TOTP code step is inline (shown only when 2FA is enabled)
4. `04-library.html` — library home screen (post-login landing)
5. `09-account-settings.html` — 2FA setup: QR code display + verification code entry

Note: password reset screens are deferred to Phase 3 — they require email delivery infrastructure (SMTP / SendGrid) not available until Azure VM deployment.

---

## Gate

UI prototype is complete when:
- [ ] All key screens identified and agreed against the PRD user stories
- [ ] Every screen has a working HTML prototype
- [ ] User flow diagram covers all paths (happy + error)
- [ ] Prototype reviewed and feedback incorporated

---

## Handoff

After prototype is agreed, proceed to:
- `/architect` — the Architect runs the four specialist architecture views with screen + flow as context

If this is a Product Discovery run and the design system has not been established yet, run `/design-system` first, then return to this skill.
