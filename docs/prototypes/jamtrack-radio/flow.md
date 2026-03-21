# Jamtrack Radio — Product-Level User Flow

> **Product Discovery Step 4b** · Generated 2026-03-21 · Covers all product-level screens

---

## Screen Inventory

| # | File | Screen | Primary action | Personas |
|---|------|--------|---------------|----------|
| 01 | `01-welcome.html` | Welcome / Landing | Choose Sign In or Create Account | All |
| 02 | `02-register.html` | Registration | Create account with email + password | New user |
| 03 | `03-login.html` | Login | Sign in (3 states: credentials → 2FA → backup code) | Returning user |
| 04 | `04-library.html` | Library | Browse, search, filter, play tracks | Musician |
| 05 | `05-upload-track.html` | Upload Track | Upload file + enter metadata (3 states: form → progress → success) | Musician |
| 06 | `06-player.html` | Track Detail / Player | Full player with waveform, track info, add to playlist | Musician |
| 07 | `07-playlists.html` | Playlists | List, create, rename, delete playlists | Musician |
| 08 | `08-playlist-detail.html` | Playlist Detail | View tracks, play all, reorder (drag or arrows), remove tracks | Musician |

---

## User Flow Diagram

```mermaid
flowchart TD
    START([Open app]) --> WELCOME[01 · Welcome\nSign In / Create Account CTAs]

    WELCOME -->|"Create Account"| REGISTER[02 · Register\nEmail · Password · Display name]
    WELCOME -->|"Sign In"| LOGIN_CREDS[03a · Login — Credentials\nEmail + password]

    REGISTER -->|"Form valid → account created"| LIBRARY
    REGISTER -->|"Already have account"| LOGIN_CREDS

    LOGIN_CREDS -->|"Valid credentials, no 2FA"| LIBRARY[04 · Library\nTrack list + search + filters + player bar]
    LOGIN_CREDS -->|"Valid credentials, 2FA enabled"| LOGIN_2FA[03b · Login — TOTP\n6-digit Google Authenticator code]
    LOGIN_CREDS -->|"Invalid credentials"| LOGIN_ERR[03a · Login — Error state\nShow error alert, retry]
    LOGIN_ERR -->|"Retry"| LOGIN_CREDS

    LOGIN_2FA -->|"Correct code"| LIBRARY
    LOGIN_2FA -->|"Wrong code (000000)"| TOTP_ERR[03b · TOTP Error state\nHighlight digits, retry]
    TOTP_ERR -->|"Retry"| LOGIN_2FA
    LOGIN_2FA -->|"Lost phone"| LOGIN_BACKUP[03c · Login — Backup Code\n8-character backup code]
    LOGIN_BACKUP -->|"Valid backup code"| LIBRARY
    LOGIN_BACKUP -->|"Invalid code"| LOGIN_BACKUP

    LIBRARY -->|"Click ⬆️ Upload"| UPLOAD_FORM[05a · Upload — Form\nDrop zone + metadata fields]
    LIBRARY -->|"Click track row"| LIBRARY_PLAY[04 · Library — Playing state\nPlayer bar appears, seek advances]
    LIBRARY -->|"Click Playlists"| PLAYLISTS
    LIBRARY -->|"Click track ▶ detail"| PLAYER

    UPLOAD_FORM -->|"Form valid + submit"| UPLOAD_PROGRESS[05b · Upload — Progress\nAnimated progress bar + step indicators]
    UPLOAD_FORM -->|"Form invalid"| UPLOAD_ERR[05a · Upload — Validation errors\nInline error messages]
    UPLOAD_ERR -->|"Fix & resubmit"| UPLOAD_FORM
    UPLOAD_PROGRESS -->|"Upload complete"| UPLOAD_SUCCESS[05c · Upload — Success\nTrack ready confirmation]
    UPLOAD_SUCCESS -->|"Go to Library"| LIBRARY
    UPLOAD_SUCCESS -->|"Upload Another"| UPLOAD_FORM

    PLAYER[06 · Track Detail / Player\nWaveform · controls · metadata · add to playlist] -->|"Add to playlist"| PLAYER_PL_ADD[06 · Add to Playlist\nInline confirmation toast]
    PLAYER_PL_ADD --> PLAYER
    PLAYER -->|"Back / breadcrumb"| LIBRARY

    PLAYLISTS[07 · Playlists\nPlaylist grid + create form] -->|"+ New Playlist → fill name → Create"| PLAYLISTS_CREATED[07 · Playlists — New card added\nToast confirmation]
    PLAYLISTS_CREATED --> PLAYLISTS
    PLAYLISTS -->|"Click playlist card"| PL_DETAIL[08 · Playlist Detail\nOrdered track list]
    PLAYLISTS -->|"⋯ → Rename"| PLAYLISTS_RENAME[07 · Rename dialog\nbrowser prompt]
    PLAYLISTS -->|"⋯ → Delete"| PLAYLISTS_DELETE[07 · Delete confirm\nbrowser confirm]
    PLAYLISTS_RENAME --> PLAYLISTS
    PLAYLISTS_DELETE --> PLAYLISTS

    PL_DETAIL -->|"▶ Play All"| PL_PLAYING[08 · Playlist Detail — Playing\nPlayer bar + advancing seek]
    PL_DETAIL -->|"Drag row / ▲▼ arrows"| PL_REORDER[08 · Reordered track list\nToast confirmation]
    PL_DETAIL -->|"🗑️ Remove track"| PL_REMOVED[08 · Track removed\nUpdated list + meta count]
    PL_DETAIL -->|"Back / Playlists breadcrumb"| PLAYLISTS
    PL_REORDER --> PL_DETAIL
    PL_REMOVED --> PL_DETAIL
```

---

## Happy Path Summary

1. New user: `Welcome → Register → Library`
2. Returning user (no 2FA): `Welcome → Login → Library`
3. Returning user (2FA): `Welcome → Login → TOTP code → Library`
4. Upload a track: `Library → Upload (drop file + metadata) → Progress → Success → Library`
5. Play a track: `Library → click row → Player bar appears → seek advances`
6. View track detail: `Library → Track detail/Player → waveform plays → Add to playlist`
7. Manage playlists: `Library → Playlists → New Playlist → Playlist Detail → Reorder / Play`

---

## Error Paths

| Screen | Error | Response |
|--------|-------|----------|
| Register | Empty field / invalid email / passwords don't match | Inline validation error per field |
| Login | Empty field | Inline field error |
| Login | Wrong password | Alert banner, retry |
| Login | Wrong TOTP code (000000) | Digits highlighted, retry |
| Login | Invalid backup code (INVALID1) | Error alert, retry |
| Upload | Empty title | Inline field error |
| Upload | BPM out of range | Inline field error |

---

## Prototype Notes

- **Navigation**: All links use `<a href="...">` with relative paths — open `01-welcome.html` in a browser and every button navigates correctly.
- **2FA demo**: In `03-login.html`, type any email containing `2fa` (e.g. `me@2fa.com`) to trigger the TOTP step. Enter `000000` to see the error state; any other 6 digits proceeds to the library.
- **Player**: In `04-library.html`, clicking a track activates the sticky bottom player bar with live seek progress. `06-player.html` auto-starts playback with a generated waveform.
- **Upload**: Drag any file onto the drop zone or click browse. Submitting runs a simulated progress animation → success state.
- **Playlist reorder**: In `08-playlist-detail.html`, use the ▲/▼ arrow buttons or drag rows to reorder.
