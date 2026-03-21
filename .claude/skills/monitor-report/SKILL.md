---
name: monitor-report
description: Generates a standalone HTML report aggregating health, error, and performance monitoring results. Saves to docs/monitoring-reports/YYYY-MM-DD-PR<N>-<service>.html. Run as MONITORING Step 4 after all three checks pass.
disable-model-invocation: true
argument-hint: [service name and PR number, e.g. "identity-service PR42"]
---

You are a DevOps Engineer producing a monitoring report for a Jamtrack Radio deployment. This report is the audit trail of every post-deployment health check.

If `$ARGUMENTS` is provided, parse it for the service name and PR number.

---

## Required Inputs

Collect the results from the previous three monitoring steps:

- **From `/monitor-health`**: all health check results (pass/fail per endpoint)
- **From `/monitor-errors`**: pre-deploy vs. post-deploy error rates by service
- **From `/monitor-performance`**: p50/p95/p99 latency before and after, by endpoint
- **Deployment metadata**: timestamp, PR number, image tag, deployer

---

## Output

Save to `docs/monitoring-reports/YYYY-MM-DD-PR<N>-<service>.html`.

```bash
mkdir -p docs/monitoring-reports
```

---

## Report Template

Generate a standalone HTML file using this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Monitoring Report — [Service] — [Date]</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: -apple-system, sans-serif; background: #f8f9fa; color: #212529; margin: 0; padding: 2rem; }
    .container { max-width: 1000px; margin: 0 auto; }
    .header { background: #1a1a2e; color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; }
    .header h1 { margin: 0 0 0.5rem; font-size: 1.5rem; }
    .header .meta { font-size: 0.85rem; color: #aaa; }
    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .badge-pass { background: #d4edda; color: #155724; }
    .badge-warn { background: #fff3cd; color: #856404; }
    .badge-fail { background: #f8d7da; color: #721c24; }
    .section { background: white; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
    .section h2 { margin: 0 0 1rem; font-size: 1.1rem; color: #1a1a2e; border-bottom: 2px solid #e9ecef; padding-bottom: 0.75rem; }
    table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
    th { background: #f8f9fa; text-align: left; padding: 0.6rem 0.8rem; border-bottom: 2px solid #dee2e6; }
    td { padding: 0.6rem 0.8rem; border-bottom: 1px solid #e9ecef; }
    tr:last-child td { border-bottom: none; }
    .summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
    .summary-card { background: white; border-radius: 8px; padding: 1.25rem; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
    .summary-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .summary-card .label { font-size: 0.8rem; color: #666; }
    .summary-card .value { font-size: 1.25rem; font-weight: 700; }
    .footer { text-align: center; color: #999; font-size: 0.8rem; padding: 1rem; }
  </style>
</head>
<body>
  <div class="container">

    <div class="header">
      <h1>Monitoring Report — [Service Name]</h1>
      <div class="meta">
        Deployment date: [YYYY-MM-DD HH:MM UTC] &nbsp;|&nbsp;
        PR: <a href="https://github.com/kumaran-naidoo-derivco/jamtrack-radio/pull/[N]" style="color:#7eb9ff">#[N]</a> &nbsp;|&nbsp;
        Image tag: [tag] &nbsp;|&nbsp;
        Environment: [Staging / Production]
      </div>
    </div>

    <!-- Summary cards -->
    <div class="summary-grid">
      <div class="summary-card">
        <div class="icon">🏥</div>
        <div class="value"><span class="badge badge-pass">PASS</span></div>
        <div class="label">Health Check</div>
      </div>
      <div class="summary-card">
        <div class="icon">⚠️</div>
        <div class="value"><span class="badge badge-warn">+3.2%</span></div>
        <div class="label">Error Rate Change</div>
      </div>
      <div class="summary-card">
        <div class="icon">⚡</div>
        <div class="value"><span class="badge badge-pass">+8%</span></div>
        <div class="label">p99 Latency Change</div>
      </div>
    </div>

    <!-- Health Check Results -->
    <div class="section">
      <h2>1. Health Check Results</h2>
      <table>
        <thead>
          <tr><th>Service</th><th>/health/live</th><th>/health/ready</th><th>Pod Status</th><th>Migration</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Identity Service</td>
            <td><span class="badge badge-pass">200 OK</span></td>
            <td><span class="badge badge-pass">200 OK</span></td>
            <td><span class="badge badge-pass">Running (0 restarts)</span></td>
            <td><span class="badge badge-pass">Success</span></td>
          </tr>
          <!-- Repeat for each service -->
        </tbody>
      </table>
    </div>

    <!-- Error Rate Analysis -->
    <div class="section">
      <h2>2. Error Rate Analysis</h2>
      <table>
        <thead>
          <tr><th>Service</th><th>Pre-deploy errors/hr</th><th>Post-deploy errors/hr</th><th>Change</th><th>Status</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Identity Service</td>
            <td>2</td>
            <td>2</td>
            <td>0%</td>
            <td><span class="badge badge-pass">PASS</span></td>
          </tr>
        </tbody>
      </table>
      <p style="font-size:0.85rem; color:#666; margin-top:0.75rem;">
        Top error types post-deploy: [None / list them]
      </p>
    </div>

    <!-- Performance Analysis -->
    <div class="section">
      <h2>3. Performance Analysis (Latency)</h2>
      <table>
        <thead>
          <tr><th>Service</th><th>Endpoint</th><th>p50 before→after</th><th>p95 before→after</th><th>p99 before→after</th><th>Status</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Identity</td>
            <td>RegisterUser</td>
            <td>12ms → 13ms</td>
            <td>45ms → 48ms</td>
            <td>120ms → 128ms</td>
            <td><span class="badge badge-pass">+6.7%</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Overall Verdict -->
    <div class="section">
      <h2>4. Overall Verdict</h2>
      <p><strong>Status: <span class="badge badge-pass">DEPLOYMENT HEALTHY — PROCEED</span></strong></p>
      <p style="margin-top:0.75rem; font-size:0.95rem;">
        [Brief narrative: "All services healthy. Error rate unchanged. p99 latency within 10% of baseline. No regressions detected. Proceeding to /retrospective."]
      </p>
    </div>

    <!-- Notes / Observations -->
    <div class="section">
      <h2>5. Notes & Observations</h2>
      <ul>
        <li>[Any notable observations that don't constitute a failure]</li>
        <li>[Action items for the retrospective]</li>
      </ul>
    </div>

    <div class="footer">
      Generated by /monitor-report skill · Jamtrack Radio · [Date]
    </div>

  </div>
</body>
</html>
```

---

## Gate

Report is complete when:
- [ ] File saved to `docs/monitoring-reports/YYYY-MM-DD-PR<N>-<service>.html`
- [ ] All three monitoring sections populated with real data
- [ ] Overall verdict clearly stated (PASS / WARNING / FAIL)
- [ ] Notable observations and action items documented

---

## Handoff

After report is saved, proceed to `/retrospective`.
