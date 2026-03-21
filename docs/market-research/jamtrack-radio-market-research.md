# Market Research: Jamtrack Radio

**Date**: 2026-03-21
**Author**: Kumaran Naidoo
**Status**: Complete

---

## 1. Market Context

Jamtrack Radio is a **personal music practice library**, not a commercial streaming service. The target user — a solo musician or hobbyist producer — wants to self-host a private library of their own recordings and backing tracks, with rich musical metadata (BPM, key, genre, tags), accessible from any device via a browser.

The "market" here is the set of tools musicians and producers currently use to solve this problem, ranging from consumer streaming platforms to local file management. The research question is:

> **What do musicians currently use to organise and stream their own private recordings, and what gaps remain unaddressed?**

The strategic lens is: **what can we learn from these tools to make Jamtrack Radio better?**

---

## 2. Competitive Landscape

### 2.1 Consumer Streaming Platforms

#### SoundCloud

| Dimension | Detail |
|-----------|--------|
| Primary use case | Public music sharing and discovery |
| Private library support | Yes — private tracks and private links |
| Free tier | 3 hours of uploads; no metadata richness |
| Paid tier | SoundCloud Next Pro (£11–22/month) for unlimited uploads |
| Musical metadata | Genre and tags only — no BPM, no musical key |
| Self-hosted? | No — vendor-hosted only |
| Streaming quality | 128kbps (free) / 256kbps (paid) |
| Key strength | Waveform scrubber with comment markers; large community |
| Key weakness for our use case | Vendor lock-in; no BPM/key metadata; public-first design |

#### Spotify (Deprecated Private Sessions)

| Dimension | Detail |
|-----------|--------|
| Primary use case | Commercial music streaming |
| Private library support | Had private sessions — deprecated 2022; local files feature limited |
| Musical metadata | Key and BPM available in API but not user-editable |
| Self-hosted? | No |
| Key weakness for our use case | Completely unsuitable — not designed for user-uploaded content |

#### Apple Music

| Dimension | Detail |
|-----------|--------|
| Private library support | iCloud Music Library — syncs local files across Apple devices |
| Musical metadata | BPM support in iTunes/Music app; no custom key or tags |
| Self-hosted? | No — Apple ecosystem only |
| Key weakness for our use case | Apple-only; no browser access; no custom tagging |

---

### 2.2 Music Creation and Collaboration Platforms

#### BandLab

| Dimension | Detail |
|-----------|--------|
| Primary use case | Online music creation, collaboration, and social sharing |
| Private library support | Private tracks supported |
| Musical metadata | BPM and key on projects; limited tagging |
| Self-hosted? | No |
| Mobile support | Excellent — mobile-first design; iOS and Android apps |
| Key strength | Clean, modern mobile UX; seamless recording-to-library workflow |
| Key weakness for our use case | Social/collaborative focus; not designed as a private archive tool |

#### Soundtrap (by Spotify)

| Dimension | Detail |
|-----------|--------|
| Primary use case | Browser-based DAW with collaboration |
| Private library support | Within-project storage only; not a standalone library |
| Musical metadata | Project BPM only; no track-level tagging |
| Self-hosted? | No |
| Key weakness for our use case | DAW product, not a library/streaming tool |

---

### 2.3 Local and DIY Solutions

#### Google Drive + Manual Organisation

| Dimension | Detail |
|-----------|--------|
| Primary use case | General file storage |
| Private library support | Yes — all files are private |
| Musical metadata | None — filename only |
| Streaming | Basic in-browser audio playback; no seek/progress control |
| Self-hosted? | No — Google-hosted |
| Cost | Free up to 15GB; £1.99/month for 100GB |
| Key weakness | Zero metadata; no filtering; no playback controls; no tagging |

#### Local Disk + Audacity / VLC

| Dimension | Detail |
|-----------|--------|
| Primary use case | Local recording and playback |
| Private library support | Completely private — on your machine |
| Musical metadata | ID3 tags supported but manual; no BPM/key extraction |
| Streaming | Local only; no multi-device access |
| Self-hosted? | Fully — but only accessible on the local machine |
| Key weakness | No remote access; no filtering; no playlists with ordering |

#### GarageBand / Logic Pro Library (macOS)

| Dimension | Detail |
|-----------|--------|
| Primary use case | Professional DAW and project management |
| Musical metadata | BPM and key stored per project; extensive tagging in Logic |
| Private library support | Fully private — local only |
| Streaming | Local only; no browser playback |
| Self-hosted? | macOS only |
| Key strength | Richest metadata model of any tool reviewed |
| Key weakness for our use case | macOS only; not self-hosted over network; no browser streaming |

#### Dropbox + Third-Party Player

| Dimension | Detail |
|-----------|--------|
| Primary use case | File sync and sharing |
| Streaming | Preview only — no seek, no persistent playback state |
| Musical metadata | None |
| Self-hosted? | No — Dropbox-hosted |

---

## 3. Feature Comparison Matrix

| Feature | SoundCloud | BandLab | GarageBand | Google Drive | Jamtrack Radio (target) |
|---------|-----------|---------|-----------|--------------|------------------------|
| Private upload | ✅ (paid) | ✅ | ✅ | ✅ | ✅ |
| BPM metadata | ❌ | ⚠️ (project) | ✅ | ❌ | ✅ |
| Musical key | ❌ | ⚠️ (project) | ✅ | ❌ | ✅ |
| Custom tags | ⚠️ (genre only) | ❌ | ✅ | ❌ | ✅ |
| Playlist management | ❌ | ⚠️ | ❌ | ❌ | ✅ |
| Browser streaming with seek | ✅ | ✅ | ❌ | ⚠️ | ✅ |
| Multi-device access | ✅ | ✅ | ❌ | ✅ | ✅ |
| Self-hosted / no vendor lock-in | ❌ | ❌ | ✅ (local) | ❌ | ✅ |
| OAuth social login | ✅ | ✅ | N/A | ✅ | ✅ |
| Cover artwork | ✅ | ✅ | ✅ | ❌ | ✅ |
| Filter by BPM/key/tag | ❌ | ❌ | ⚠️ (local) | ❌ | ✅ |
| HTTP Range streaming (seek) | ✅ | ✅ | N/A | ❌ | ✅ |
| Open source / self-hostable | ❌ | ❌ | ❌ | ❌ | ✅ |

**Key:** ✅ Full support · ⚠️ Partial / limited · ❌ Not supported

---

## 4. Differentiation Analysis

### What Jamtrack Radio Does That No Single Competitor Does

1. **Self-hosted + streaming + rich metadata together** — GarageBand has rich metadata but no streaming; SoundCloud has streaming but no BPM/key; Google Drive has multi-device but no metadata. Jamtrack Radio combines all three.

2. **Musical metadata as first-class citizens** — BPM, musical key, and custom tags are indexed and filterable. No competitor except GarageBand supports this combination, and GarageBand is local-only.

3. **No vendor lock-in** — the operator owns the infrastructure. Tracks cannot be taken down by a platform policy change or a pricing model shift.

4. **Designed for the learning-project context** — the codebase is a portfolio-grade cloud-native system covering the full stack. No comparable tool teaches its own architecture.

### What Competitors Do Better (Lessons to Incorporate)

| Competitor | Lesson | How to apply |
|------------|--------|-------------|
| SoundCloud | Waveform scrubber with visual seek — users orient themselves in a track quickly | Phase 7: consider waveform visualisation on the player screen |
| BandLab | Mobile-first UX — clean card-based layout, large tap targets, instant feedback | Prototype screens already reflect this pattern |
| GarageBand / Logic | Richest metadata model: BPM, key, time signature, tags, colour labels | Use as the baseline for Jamtrack Radio's metadata schema |
| SoundCloud | Playback quality tiers (128 / 256kbps) | Phase 3 backlog: offer compressed alternative for low-bandwidth streaming |
| BandLab | Social "like" + comment markers on waveform | Out of scope for v1; note as a v2 feature candidate |
| Google Drive | Zero-friction upload — drag and drop, no form required | Phase 2+: consider drag-and-drop upload as an enhancement |

---

## 5. Market Positioning

**Jamtrack Radio's positioning statement:**

> "The only self-hosted, privacy-first music practice library that lets solo musicians upload, organise, and stream their own tracks with full musical metadata — BPM, key, genre, and custom tags — from any device, with zero vendor dependency."

**Target positioning quadrant:**

|  | Low metadata richness | High metadata richness |
|--|----------------------|----------------------|
| **Vendor-hosted** | Google Drive, Dropbox | GarageBand (Apple ecosystem) |
| **Self-hosted / open** | Local disk + VLC | **Jamtrack Radio** ← target position |

---

## 6. Strategic Conclusions

1. **The gap is real**: No tool combines self-hosting + HTTP streaming + rich musical metadata. The closest is a self-managed Subsonic/Navidrome setup, but those are general music servers without practice-specific metadata (BPM, key) as primary features.

2. **Scope is correct**: The PRD's scope (upload, metadata, playlists, streaming, OAuth) directly addresses the features that competitors either miss or charge for.

3. **The metadata schema is the differentiator**: BPM, musical key, and custom tags must be indexed and filterable from day one. This is the primary reason a musician would choose Jamtrack Radio over Google Drive.

4. **UX inspiration**: Take BandLab's mobile-first card layout (already reflected in prototype screens) and SoundCloud's streaming UX (seek bar, playback speed, time markers).

5. **Build vs. Buy for audio streaming**: HTTP range request streaming is a standard browser feature — no third-party streaming CDN is needed for a personal-scale library. This is a feature, not a dependency.

6. **Self-hosting is the moat**: The feature no competitor offers is operator ownership. This is the kill condition for vendor-hosted competitors from the operator's perspective.
