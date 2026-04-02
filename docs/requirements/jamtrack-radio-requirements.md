# Requirements: Jamtrack Radio

**Date**: 2026-03-21
**Author**: Kumaran Naidoo
**Status**: Agreed

---

## 1. Problem Statement

Solo musicians and hobbyist producers who record jam sessions, practice tracks, and compositions have no self-hosted, privacy-first platform with rich musical metadata. Consumer streaming services (Spotify, SoundCloud) are designed for public publishing, not private personal libraries. There is no accessible tool that lets a musician upload tracks with structured metadata (BPM, key, genre, tags), organise them into playlists, and stream from any device — without relying on a third-party SaaS provider that may change pricing, restrict uploads, or expose data.

Beyond the product need, the platform serves as the primary vehicle for learning modern cloud-native engineering: microservices, containers, Kubernetes, CI/CD, multi-cloud deployment, and observability. No single existing tutorial or course covers this combination of competencies end-to-end on a real codebase.

**Evidence of the problem:**
- Spotify deprecated its private session feature in 2022, leaving musicians without a streaming option for personal libraries
- SoundCloud's free tier limits uploads to 3 hours; private hosting requires a paid plan (£11–£22/month)
- Musicians resort to unstructured Google Drive folders or local Audacity libraries — no metadata, no streaming, no multi-device access

---

## 2. Target Personas

### Persona 1 — Practising Guitarist / Solo Musician

| Attribute | Detail |
|-----------|--------|
| Name | Alex (composite) |
| Role | Semi-professional guitarist, regular practice sessions |
| Goal | Organise a personal library of jam backing tracks by BPM, key, and genre; find the right track instantly during practice |
| Pain today | Tracks live in an unstructured Google Drive folder or local disk. Finding the right key/BPM backing track mid-session requires manually scanning filenames. Can't access from tablet without file transfer. |
| Success | Filters to "minor blues, BPM 70–80, key Am" in under 10 seconds and hits play instantly from any device |

### Persona 2 — Hobbyist Producer / Session Recorder

| Attribute | Detail |
|-----------|--------|
| Name | Sam |
| Role | Home studio hobbyist, records original sessions and experiments |
| Goal | Archive recordings with rich metadata (title, BPM, key, genre, tags, artwork); stream without downloading; never lose a recording again |
| Pain today | Records in Audacity, saves to local disk with no metadata beyond filename. No access from phone or tablet. No search or filter capability. |
| Success | Every recording has title, BPM, key, genre, and custom tags. Accessible from any device; playback starts within 2 seconds. |

### Persona 3 — Cloud-Native Learner (Operator / Builder)

| Attribute | Detail |
|-----------|--------|
| Name | Kumaran Naidoo |
| Role | Experienced architect (21 yrs dev, 4 yrs architect) expanding into cloud-native full-stack |
| Goal | Build a production-grade cloud-native application end-to-end, demonstrating mastery of microservices, Docker, K8s, Terraform, Azure, AWS, CI/CD, ELK |
| Pain today | Hands-on experience with this stack only comes from expensive commercial projects (no access for solo learning) or shallow tutorials (no real complexity) |
| Success | All 7 phases complete; system deployed to Azure AKS and AWS EKS; structured logs visible in ELK dashboard; CI green on main; portfolio demonstrating every listed skill |

---

## 3. Constraints

### Technical Constraints

| Constraint | Detail |
|------------|--------|
| Platform | Windows 11 + WSL 2 (Ubuntu) as primary development environment |
| Cloud — Azure | Active subscription; primary cloud platform from Phase 4 |
| Cloud — AWS | No current account; to be created in Phase 5 |
| Language / runtime | C# / ASP.NET Core for all services; no alternative runtime |
| Data access | Dapper (SQL-first micro-ORM) + FluentMigrator (versioned migrations); no EF Core |
| Internal API | gRPC for all service-to-service communication |
| Server-side architecture | Clean Architecture mandatory: Domain → Application → Infrastructure / Api |
| Container runtime | Docker (local dev); Rancher Desktop K8s (local K8s); AKS (Azure); EKS (AWS) |
| CI/CD | GitHub Actions only |
| VCS | GitHub (HTTPS primary; SSH configured as fallback) |
| Auth | RS256 JWT (access tokens, 15 min expiry) + refresh tokens; OAuth 2.0 via Google / Apple / Facebook |

### Scope Constraints

- **Self-hosted / personal use only** — no multi-tenant SaaS; no commercial licensing
- **No commercial music** — tracks assumed to be owned or licensed by the uploader; no DRM required
- **Single user initially** — system designed to scale horizontally but v0.1 targets single-user operation

### Budget Constraints

| Phase | Infra cost |
|-------|-----------|
| Phase 0–3 (local dev) | £0 — runs entirely on local hardware |
| Phase 4 (Azure) | ~£50–100/month target (personal subscription, burstable/spot VMs preferred) — see reconciliation note below |
| Phase 5 (AWS) | ~£50–100/month additional — leverage Free Tier where available |

> **Budget reconciliation** (updated 2026-04-01 after cloud architecture was completed):
> The cloud architecture (see `docs/architecture/jamtrack-radio/cloud-arch.md`) shows a realistic Phase 4 staging cost of **~£197/month** and production baseline of **~£1,142/month** — both higher than the £50–100/month target above.
>
> The discrepancy arises because the original budget was a rough pre-architecture estimate that did not account for AKS node sizing, Log Analytics ingestion, or Application Gateway/WAF. The cloud architecture uses always-on staging with burstable nodes; the £50–100 target assumed a more aggressive teardown schedule.
>
> **Resolution**: The £50–100/month constraint is relaxed to **£200–300/month for staging** (apply node auto-stop outside business hours to reduce towards the lower end). The production cost of ~£1,142/month is accepted as a necessary Phase 4 cost — the project's financial model (ROI analysis in §7) remains valid at this spend level. The cloud architecture TCO table is the authoritative source from Phase 4 planning onwards.

### Non-Negotiable Decisions

- Never commit directly to `main` — all changes via branch → PR → CI → squash merge
- Conventional Commits spec for all commit messages (`feat:`, `fix:`, `docs:`, `chore:`, etc.)
- Each task = GitHub Issue; each phase = GitHub Milestone
- Branch naming convention: `kumarann/<type>/<description>`

---

## 4. Success Metrics

| KPI | Target | How Measured |
|-----|--------|--------------|
| End-to-end upload-to-stream | Complete within 5 minutes of account creation | Manual integration test on deployed system |
| Streaming latency (TTFB) | < 2 seconds at p95 on standard broadband | Load test in Phase 4 (Azure) |
| Cross-user data isolation | Zero cross-user access — all cross-user requests return 403 | Integration test suite asserting 403 on every cross-user endpoint |
| CI green on main | 100% of merged PRs pass the `build` check | GitHub Actions status; enforced by branch protection |
| Phase delivery | All 7 phases reach "Complete" milestone closure | GitHub milestone closure |
| Observability | Structured logs from all services visible in ELK dashboard after Phase 6 | Manual dashboard verification |
| Architecture compliance | All server-side services pass Clean Architecture dependency rule check | Code review gate on every PR |

---

## 5. Value Prediction

> **Context**: Jamtrack Radio is a personal learning project with no commercial revenue stream. The financial model below quantifies the opportunity cost of the investment and the expected return in career advancement and professional skill value — treating the project as a structured investment in professional development.

| Item | Estimate | Assumption |
|------|----------|------------|
| Estimated build effort | ~190 developer-days across all 7 phases | Phased delivery at 4–8 productive hours/day |
| Build cost (opportunity cost) | £95,000 | At mid-market contractor rate of £500/day |
| Ongoing opex — Phase 4 onwards | £197–256/month staging; £1,142/month prod (Azure) | Cloud architecture TCO (2026-04-01); staging with node auto-stop targets £200–300/month |
| Ongoing opex — Phase 5 onwards | +£50–100/month (AWS) | Free Tier where available |
| Annual infra cost from Phase 4 | ~£1,200–2,400/year | Azure + AWS combined |
| Equivalent training courses foregone | £6,000–10,000 | CKA (£500), AZ-104 (£1,500), K8s/microservices bootcamp (£3,000–5,000), cloud-native course (£1,000–3,000) |
| Expected career rate increase | £50–100/day | Demonstrated full-stack cloud-native portfolio at senior architect level |
| Expected annual benefit from rate uplift | £12,500–25,000/year | 250 contract days/year × rate increase |
| Payback period | From Phase 4 completion | Skills directly applicable to live client engagements |
| ROI at 12 months post-Phase 7 | ~270–430% | (£15,000 benefit – £2,400 opex) ÷ £2,400 opex |
| ROI at 24 months post-Phase 7 | ~490–700% | Cumulative benefit vs cumulative opex |
| Confidence level | Medium | Skill acquisition: High confidence. Rate impact: Medium (market-dependent). |

### Viability Threshold

The project is worth building if we reach **Phase 4 (Azure AKS deployment) with all three core services running** — Identity, Track, and Streaming. At that point the portfolio demonstrates the full cloud-native microservices stack across Docker, K8s, and a managed cloud, regardless of whether Phases 5–7 complete.

Secondary threshold: If Phase 3 (Dockerised + local K8s) is reached but time constraints prevent further progress, the containerisation and orchestration skills alone represent a meaningful portfolio addition.

### Kill Condition

Not applicable — this is a personal learning project with no revenue dependency. If scope must be reduced, the project **pivots** (reduces feature scope or skips a phase) rather than terminates. The minimum viable portfolio outcome is Phase 3 complete with all services running in local Kubernetes.

---

## 6. Open Questions

| Question | Owner | Target Resolution |
|----------|-------|-------------------|
| Apple OAuth requires a paid Apple Developer account (£99/year). Confirm availability before implementing OAuth providers in Phase 4. | Kumaran | Phase 3 planning |
| Frontend framework: React vs Blazor. API must remain frontend-agnostic from Phase 2 onwards. Decision can be deferred until Phase 7. | Kumaran | Phase 6 planning |
| Audio transcoding: should the platform transcode uploads to MP3 320kbps on ingest? Would require a worker/queue job. Evaluate as Phase 3 backlog item. | Kumaran | Phase 3 backlog |
| Full-text track search: PostgreSQL `tsvector` sufficient, or introduce Elasticsearch from the ELK stack? Evaluate during Phase 6. | Kumaran | Phase 6 planning |
| Storage cost model: Azure Blob vs S3 pricing at scale for audio files. Evaluate during Phase 4/5. | Kumaran | Phase 4/5 planning |
