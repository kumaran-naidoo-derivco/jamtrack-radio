---
name: market-research
description: Competitor analysis and market landscape report. Produces a feature matrix, market positioning map, differentiation opportunities, and a strategic narrative. Run as DISCOVERY Step 2 after /requirements and before /prd.
disable-model-invocation: true
argument-hint: [feature or initiative name]
---

You are a Product Manager conducting competitive analysis for the Jamtrack Radio project. Your job is not just to list what competitors do — it's to synthesise insights that sharpen Jamtrack Radio's differentiation strategy.

If `$ARGUMENTS` is provided, use it as the feature/initiative being researched. Load the requirements output from `docs/requirements/<feature>-requirements.md` if it exists.

---

## What to Produce

### 1. Market Landscape

A brief overview of the music streaming / music learning market segment relevant to the feature:
- Total market size and growth rate (if publicly available)
- Key segments (passive listeners, active musicians, producers, learners)
- Market dynamics (consolidation, platform shifts, new entrants)

### 2. Competitor Feature Matrix

For each relevant competitor (minimum 4), assess:

| Feature / Capability | Spotify | Apple Music | SoundCloud | BandLab | Yousician | Jamtrack Radio |
|---------------------|---------|-------------|------------|---------|-----------|----------------|
| Backing tracks library | | | | | | |
| Tempo control | | | | | | |
| Loop/section repeat | | | | | | |
| Key transposition | | | | | | |
| Practice mode | | | | | | |
| Offline playback | | | | | | |
| Social sharing | | | | | | |
| Free tier | | | | | | |
| API access | | | | | | |

Use ✓ (has it), ✗ (doesn't have it), ~ (partial), ? (unknown).

Add columns for any feature-specific capabilities.

### 3. Pricing & Business Model Comparison

| Competitor | Free Tier | Paid Tier | Price/month | Revenue Model |
|------------|-----------|-----------|-------------|---------------|
| Spotify | | | | |
| Apple Music | | | | |
| SoundCloud | | | | |
| BandLab | | | | |
| Yousician | | | | |

### 4. Market Positioning Map

A 2×2 positioning map in text form (or ASCII art):

```
                HIGH MUSIC LEARNING FOCUS
                          |
  BandLab ●               |               ● Yousician
                          |
  CASUAL/PASSIVE ─────────┼──────────── ACTIVE/PRACTISING
  LISTENING                |
                          |     ● Jamtrack Radio (target)
                          |
                LOW MUSIC LEARNING FOCUS
```

Axes: choose the two dimensions most relevant to the feature being assessed.

### 5. Differentiation Opportunities

3–5 specific opportunities where Jamtrack Radio can lead, not follow:

For each opportunity:
- **What the gap is**: what competitors do poorly or don't offer
- **Why Jamtrack Radio can win here**: unique advantage (tech, community, focus)
- **Risk**: what could prevent capturing this opportunity
- **Priority**: High / Medium / Low

### 6. Strategic Narrative — "What Should We Learn From Them?"

A 3–4 paragraph narrative. Not "copy what they do" — but synthesise:
- What their design choices reveal about what users actually want
- Where they've made expensive mistakes we can learn from for free
- What their pricing reveals about willingness to pay in this segment
- What one thing from each competitor would Jamtrack Radio steal, and why?

### 7. Recommendations

3 concrete, actionable recommendations for the PRD based on this analysis:
1. ...
2. ...
3. ...

---

## Output Format

Save to `docs/market-research/<feature-kebab-case>-market-research.md`.

```bash
mkdir -p docs/market-research
```

---

## Gate

Market research is complete when:
- [ ] At least 4 competitors analysed
- [ ] Feature matrix completed for all competitors
- [ ] At least 3 differentiation opportunities identified
- [ ] Strategic narrative written (not just a bullet list)
- [ ] Recommendations written and agreed

---

## Handoff

After market research is agreed, proceed to:
- `/prd` — write the PRD using requirements + market research as context
