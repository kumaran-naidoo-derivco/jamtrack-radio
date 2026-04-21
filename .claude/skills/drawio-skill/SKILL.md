---
name: drawio
description: Create and edit draw.io diagram files for architecture diagrams, flowcharts, network diagrams, and technical illustrations. Use when the user asks to create diagrams, architecture visuals, flowcharts, wireframes, network topology, or any visual that should be editable in draw.io/diagrams.net. Outputs .drawio source files and .drawio.svg embedded SVGs for inline GitHub rendering.
---

# Draw.io Diagram Skill

Create professional, editable diagram files in draw.io's native XML format.

## File Format Standard

Every diagram is a **single file**: `<name>.drawio.svg`

| Property | Detail |
|----------|--------|
| Renders inline | GitHub markdown, VS Code markdown preview |
| Editable | Open directly in VS Code with the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) extension — source XML is embedded |
| White background | Set explicitly so diagrams are readable in VS Code dark mode and GitHub light mode |

No separate `.drawio` source file needed — the SVG already contains the full draw.io XML.

The SVG is exported with an explicit white background so it renders as a self-contained diagram in any context — VS Code dark mode, GitHub light mode, browser. No CSS tricks needed.

**Embedding in markdown:**
```markdown
![Diagram title](diagrams/name.drawio.svg)

> _Edit: open [`name.drawio.svg`](diagrams/name.drawio.svg) directly in VS Code with the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) extension — it opens `.drawio.svg` files natively. No separate `.drawio` file needed._
```

## Export `.drawio` → `.drawio.svg` (Docker)

Uses the `rlespinasse/drawio-export` Docker image (pull once: `docker pull rlespinasse/drawio-export:latest`).

```bash
DIAGRAMS_DIR="<absolute-path-to-diagrams-folder>"

# Wrap bare mxGraphModel files (only needed if file lacks <mxfile> wrapper)
python3 << 'EOF'
import os, uuid
path = f"{os.environ['DIAGRAMS_DIR']}/<name>.drawio"
content = open(path).read().strip()
if not content.startswith('<mxfile'):
    wrapped = f'<mxfile host="app.diagrams.net">\n    <diagram id="{uuid.uuid4().hex[:20]}" name="Page-1">\n        {content}\n    </diagram>\n</mxfile>'
    open(path, 'w').write(wrapped)
EOF

# Export as embedded SVG
docker run --rm \
  -v "${DIAGRAMS_DIR}:/data" \
  rlespinasse/drawio-export:latest \
  --format svg \
  --embed-diagram \
  --remove-page-suffix \
  --output /data/svg-export \
  "/data/<name>.drawio"

# Rename output to .drawio.svg
mv "${DIAGRAMS_DIR}/svg-export/<name>.svg" "${DIAGRAMS_DIR}/<name>.drawio.svg"
rmdir "${DIAGRAMS_DIR}/svg-export" 2>/dev/null || true
```

**Batch export all `.drawio` files in a folder:**
```bash
DIAGRAMS_DIR="<absolute-path-to-diagrams-folder>"
FILES=(context containers domain-identity er-diagram data-flow)  # no extension

# Step 1 — Ensure <mxfile> wrapper (needed if file starts with bare <mxGraphModel>)
python3 << 'PYEOF'
import os, uuid
diagrams_dir = "<absolute-path-to-diagrams-folder>"
files = ["context", "containers", "domain-identity", "er-diagram", "data-flow"]
for name in files:
    path = f"{diagrams_dir}/{name}.drawio"
    c = open(path, encoding="utf-8").read().strip()
    if not c.startswith("<mxfile"):
        wrapped = f'<mxfile host="app.diagrams.net">\n    <diagram id="{uuid.uuid4().hex[:20]}" name="Page-1">\n        {c}\n    </diagram>\n</mxfile>'
        open(path, "w", encoding="utf-8").write(wrapped)
        print(f"Wrapped: {name}.drawio")
PYEOF

# Step 2 — Export as embedded SVG (light theme base)
for f in "${FILES[@]}"; do
  docker run --rm \
    -v "${DIAGRAMS_DIR}:/data" \
    rlespinasse/drawio-export:latest \
    --format svg --embed-diagram --remove-page-suffix \
    --output /data/svg-export "/data/${f}.drawio"
  mv "${DIAGRAMS_DIR}/svg-export/${f}.svg" "${DIAGRAMS_DIR}/${f}.drawio.svg"
done
rmdir "${DIAGRAMS_DIR}/svg-export" 2>/dev/null || true

# Step 3 — Ensure explicit white background (renders correctly in VS Code dark mode and GitHub)
python3 << 'PYEOF'
import os, re
diagrams_dir = "<absolute-path-to-diagrams-folder>"
for filename in os.listdir(diagrams_dir):
    if not filename.endswith(".drawio.svg"):
        continue
    path = os.path.join(diagrams_dir, filename)
    content = open(path, encoding="utf-8").read()
    content = re.sub(
        r'background:\s*[^;]+;?\s*background-color:\s*[^;]+;?',
        'background: white; background-color: white;',
        content
    )
    open(path, "w", encoding="utf-8").write(content)
    print(f"Patched: {filename}")
PYEOF

# Step 4 — Restore wrapped .drawio source files (git repo only)
git restore <space-separated .drawio filenames>
```

## Source File Format

Draw.io source files are XML with this structure:

```xml
<mxfile host="app.diagrams.net" modified="DATE" agent="Claude" version="21.0.0" type="device">
  <diagram name="DIAGRAM_NAME" id="UNIQUE_ID">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="850" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- All diagram elements go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Core Element Types

### Azure Component with Icon Badge (preferred pattern for cloud services)

Rounded rectangle carries the readable label; a 24×24 Azure SVG icon child sits in the top-right corner as a resource-type indicator. Keeps logical diagram readability while showing the underlying Azure service at a glance.

```xml
<!-- Component rectangle -->
<mxCell id="apigw" value="&lt;b&gt;API Gateway&lt;/b&gt;&lt;br&gt;&lt;&lt;component&gt;&gt;&lt;br&gt;YARP · ASP.NET Core 8"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
         verticalAlign=middle;align=center;fontSize=11;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="80" as="geometry" />
</mxCell>

<!-- Azure icon badge — top-right corner, non-interactive -->
<mxCell id="apigw_icon" value=""
  style="aspect=fixed;html=1;align=center;image;pointerEvents=0;
         image=img/lib/azure2/networking/Application_Gateways.svg;"
  vertex="1" parent="apigw">
  <mxGeometry x="132" y="4" width="24" height="24" as="geometry" />
</mxCell>
```

**Icon position formula** — `x = parentWidth − 28`, `y = 4`:

| Rectangle width | Icon x |
|----------------|--------|
| 120 | 92 |
| 140 | 112 |
| 160 | 132 |
| 180 | 152 |
| 200 | 172 |

**Rules:**
- Icon is always 24×24 px
- `pointerEvents=0` — icon is non-clickable so edges connect to the rectangle, not the icon
- `parent="COMPONENT_ID"` — icon coordinates are relative to the rectangle
- Use icon badges for Azure-managed services only; plain rectangles for generic/external components
- See `references/cloud-icons.md` for the complete Azure SVG path reference

**Common Azure icon paths (`img/lib/azure2/`):**

> Paths verified against VS Code draw.io extension v1.9.0 bundled assets. Use these exact names — filenames are case-sensitive and the VS Code extension and draw.io Electron ship slightly different sets.

| Service | Path |
|---------|------|
| Application Gateway | `networking/Application_Gateways.svg` |
| Kubernetes (AKS) | `containers/Kubernetes_Services.svg` |
| PostgreSQL Flexible Server | `databases/Azure_Database_PostgreSQL_Server.svg` |
| Redis Cache | `databases/Cache_Redis.svg` |
| Blob / Storage Account | `storage/Storage_Accounts.svg` |
| Key Vault | `security/Key_Vaults.svg` |
| Entra ID / Azure AD | `identity/Azure_AD_B2C.svg` |
| Log Analytics | `manage_monitor/Log_Analytics_Workspaces.svg` |
| Service Bus | `integration/Service_Bus.svg` |
| Container Registry | `containers/Container_Registries.svg` |

---

### Component with Annotation Note (preferred pattern for multi-line labels)

When a component label contains more than 2 lines of detail, the text overflows the shape bounds and renders as a floating white box. The fix is a two-part pattern: the **shape label** carries only the service name + stereotype (1–2 lines, always fits), and a **child annotation note** carries the implementation detail as small grey text just below the shape. The child automatically moves with the parent — the same mechanism as the Azure icon badge.

```xml
<!-- Main shape — title + stereotype only (fits cleanly inside box) -->
<mxCell id="apigw" value="&lt;b&gt;API Gateway&lt;/b&gt;&lt;br&gt;&lt;&lt;component&gt;&gt;"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
         verticalAlign=middle;align=center;fontSize=11;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="60" as="geometry" />
</mxCell>

<!-- Annotation note — child of apigw, auto-moves with parent
     x=0       keeps same left edge as parent
     y=height+4  positions 4 px below the shape bottom
     width=parentWidth  aligns annotation to parent width -->
<mxCell id="apigw_note" value="YARP Reverse Proxy · ASP.NET Core 8"
  style="text;html=1;strokeColor=none;fillColor=none;align=center;
         verticalAlign=top;whiteSpace=wrap;fontSize=9;fontColor=#666666;"
  vertex="1" parent="apigw">
  <mxGeometry x="0" y="64" width="160" height="20" as="geometry" />
</mxCell>
```

**Annotation geometry rules:**

| Dimension | Value | Notes |
|---|---|---|
| `x` | `0` | Aligns left edge to parent shape |
| `y` | `parentHeight + 4` | 4 px gap below the shape bottom |
| `width` | `parentWidth` | Same width as parent for centred text |
| `height` | `20` (1 line) or `36` (2 lines) | Expand for longer annotations |

**Annotation style rules:**
- `fontSize=9;fontColor=#666666` — subdued grey, clearly secondary to the shape label
- `fillColor=none;strokeColor=none` — no background, no border (invisible container)
- `align=center;verticalAlign=top` — centred text, top-anchored in the note cell
- Use `·` (middle dot U+00B7) as a separator between items on the same line
- **Never** use `labelBackgroundColor=#ffffff` on shape labels — it creates an opaque white box. Omit this attribute entirely.

**For image-based Azure icon shapes** (75×65 px, `image=img/lib/azure2/...`):
The shape's `value=""` attribute renders as a label *below* the 65px icon bounds (same region as a child note at y=68). To avoid overlap, **set `value=""` on the icon shape and use a single child label cell** that contains both the bold service name and the grey description as HTML:

```xml
<!-- Icon shape — value="" avoids label/note overlap -->
<mxCell id="appgw" value=""
  style="aspect=fixed;html=1;points=[];align=center;image;
         image=img/lib/azure2/networking/Application_Gateways.svg;"
  vertex="1" parent="1">
  <mxGeometry x="120" y="100" width="75" height="65" as="geometry" />
</mxCell>

<!-- Combined label: bold name + grey description in one child cell.
     x=-28 centres the 130px-wide label under the 75px icon.
     y=68  positions it 3px below the icon bottom edge. -->
<mxCell id="appgw_lbl"
  value="&lt;b&gt;Azure Application Gateway&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#666666;&quot;&gt;WAF v2 · TLS 1.3 termination&lt;/font&gt;"
  style="text;html=1;strokeColor=none;fillColor=none;align=center;
         verticalAlign=top;whiteSpace=wrap;fontSize=11;"
  vertex="1" parent="appgw">
  <mxGeometry x="-28" y="68" width="130" height="36" as="geometry" />
</mxCell>
```

Icon label geometry: `x=-28, y=68, width=130, height=36`

| Dimension | Value | Notes |
|---|---|---|
| `x` | `-28` | Shifts left so 130px label is centred under 75px icon |
| `y` | `68` | 3px gap below the 65px icon height |
| `width` | `130` | Wider than icon to fit multi-word service names |
| `height` | `36` | 2 lines at 18px each (bold name + grey description) |

---

### Basic Shapes

```xml
<!-- Rectangle -->
<mxCell id="unique-id" value="Label Text" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>

<!-- Rounded Rectangle -->
<mxCell id="unique-id" value="Label" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>

<!-- Cylinder (Database) -->
<mxCell id="unique-id" value="Database" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="80" as="geometry" />
</mxCell>

<!-- Ellipse -->
<mxCell id="unique-id" value="Node" style="ellipse;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="80" as="geometry" />
</mxCell>
```

### Containers & Groups

```xml
<!-- Swimlane (Container with Header) -->
<mxCell id="unique-id" value="Section Title" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=30;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="200" height="150" as="geometry" />
</mxCell>

<!-- Header Bar (using brand primary color) -->
<mxCell id="unique-id" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0066CC;strokeColor=#0066CC;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="400" height="40" as="geometry" />
</mxCell>
```

### Connectors & Arrows

> **Routing rule**: Always include `edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto` on every connector. This routes lines in right-angle segments that navigate *around* shapes rather than through them. Add explicit `exitX/exitY/entryX/entryY` when auto-routing still crosses a shape.

```xml
<!-- Basic Arrow (default — use for all connectors) -->
<mxCell id="unique-id" value="label" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;endArrow=block;endFill=1;html=1;rounded=0;strokeWidth=1.5;strokeColor=#555555;fontColor=#444444;fontSize=10;labelBackgroundColor=none;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Bidirectional Arrow -->
<mxCell id="unique-id" value="label" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;endArrow=block;endFill=1;startArrow=block;startFill=1;html=1;rounded=0;strokeWidth=1.5;strokeColor=#555555;labelBackgroundColor=none;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Dashed Line (async / optional dependency) -->
<mxCell id="unique-id" value="label" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;endArrow=block;endFill=1;html=1;dashed=1;dashPattern=8 8;strokeColor=#999999;fontColor=#444444;fontSize=10;labelBackgroundColor=none;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Flex Arrow (Block Arrow — emphasis / bulk data) -->
<mxCell id="unique-id" value="" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;shape=flexArrow;endArrow=block;html=1;fillColor=#FFB800;strokeColor=#cc9400;width=20;endSize=8;labelBackgroundColor=none;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

#### Routing attributes — preventing line crossings

| Attribute | Value | Effect |
|---|---|---|
| `edgeStyle` | `orthogonalEdgeStyle` | Right-angle bends — lines route *around* shapes, not through them |
| `orthogonalLoop` | `1` | Prevents routing collapse when source and target are on the same side |
| `jettySize` | `auto` | Auto-calculates stub length for clean right-angle bends at connection points |
| `exitX` / `exitY` | `0`–`1` | Which side of the source shape the line leaves from |
| `entryX` / `entryY` | `0`–`1` | Which side of the target shape the line arrives at |
| `exitDx` / `entryDx` | `0` | Horizontal offset from the anchor (default 0) |

**Common exit/entry combinations:**

| Direction | `exitX;exitY` | `entryX;entryY` | Use case |
|---|---|---|---|
| Left → Right | `1;0.5` | `0;0.5` | Standard LTR data flow |
| Right → Left | `0;0.5` | `1;0.5` | Reverse / response flow |
| Top → Bottom | `0.5;1` | `0.5;0` | Vertical layer diagrams |
| Bottom → Top | `0.5;0` | `0.5;1` | Upward flow |

**No-corners rule**: Never let both coordinates sit at an extreme simultaneously — that places the connector at the corner of the shape, which looks bad. When pinning a line to a specific side, keep the *other* coordinate between `0.2` and `0.8`.

| ✗ Corner (avoid) | ✓ On-side (use instead) |
|---|---|
| `exitX=1;exitY=1` (bottom-right corner) | `exitX=1;exitY=0.8` (right side, near bottom) |
| `entryX=0;entryY=0` (top-left corner) | `entryX=0;entryY=0.2` (left side, near top) |
| `exitX=0.5;exitY=1` | ✓ OK — centre of bottom edge, not a corner |
| `entryX=1;entryY=0.5` | ✓ OK — centre of right edge, not a corner |

Rule of thumb: a connector is at a corner when **both** values are in `{0, 1}`. If only one is, you're on a face — that's fine.

**Fan-out rule — multiple edges on the same face**: When two or more edges leave (or arrive at) the same face of a shape from the same exit/entry point, they overlap until draw.io can route them apart. Fan out their `exitY` (or `entryY`) values across the face so each edge gets its own departure point.

| Edges on same face | Suggested `exitY` (or `entryY`) values |
|---|---|
| 2 edges | `0.35` and `0.65` |
| 3 edges | `0.25`, `0.5`, `0.75` |
| 4 edges | `0.2`, `0.4`, `0.6`, `0.8` |

```xml
<!-- ✗ All three overlap at exitY=0.5 of the gateway -->
<mxCell id="e-gw-a" ... style="...exitX=1;exitY=0.5;..." source="apigw" target="svc-a" />
<mxCell id="e-gw-b" ... style="...exitX=1;exitY=0.5;..." source="apigw" target="svc-b" />
<mxCell id="e-gw-c" ... style="...exitX=1;exitY=0.5;..." source="apigw" target="svc-c" />

<!-- ✓ Fanned out — each edge has its own exit point on the right face -->
<mxCell id="e-gw-a" ... style="...exitX=1;exitY=0.25;entryX=0;entryY=0.5;..." source="apigw" target="svc-a" />
<mxCell id="e-gw-b" ... style="...exitX=1;exitY=0.5;entryX=0;entryY=0.5;..." source="apigw" target="svc-b" />
<mxCell id="e-gw-c" ... style="...exitX=1;exitY=0.75;entryX=0;entryY=0.5;..." source="apigw" target="svc-c" />
```

**Edge label positioning — preventing labels from landing on shapes**: By default, draw.io places the edge label at the geometric midpoint of the routed line. If that midpoint falls over a shape, the label renders on top of the box. Fix with `<mxPoint as="offset">` inside the geometry — it shifts the label in absolute pixels from its calculated position. A negative `y` lifts the label above the line; positive pushes it below.

```xml
<!-- Label shifted 14px above the midpoint — clears any shape underneath -->
<mxCell id="e-svcb-bus" value="publish"
  style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;
         exitX=1;exitY=0.35;entryX=0;entryY=0.5;
         endArrow=block;endFill=1;html=1;rounded=0;strokeWidth=1;strokeColor=#d79b00;fontSize=10;"
  edge="1" parent="system-boundary" source="svc-b" target="msgbus">
  <mxGeometry relative="1" as="geometry">
    <mxPoint as="offset" x="0" y="-14" />
  </mxGeometry>
</mxCell>
```

Rules for label offsets:
- **Apply `y="-14"` to every labeled edge** — even when no shape is nearby. It shifts the text above the line centre so the stroke doesn't visually cut through the characters, making labels readable without a background box.
- Use `y="14"` when layout requires the label to appear below the line instead (e.g. two parallel edges that need labels on opposite sides).
- Use `x` offset to slide the label along the edge when the midpoint is too close to a shape boundary.
- Do **not** use `labelBackgroundColor=#ffffff` — it creates an opaque white box. Set `labelBackgroundColor=none` explicitly on every edge.

When auto-routing still crosses a shape, add explicit waypoints to route around it:

```xml
<mxCell id="e3" value="label" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;exitX=0.5;exitY=0;entryX=0.5;entryY=0;endArrow=block;endFill=1;html=1;strokeColor=#555555;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="200" y="100" />  <!-- waypoint above the obstructing shape -->
      <mxPoint x="500" y="100" />
    </Array>
  </mxGeometry>
</mxCell>
```

### Text Elements

```xml
<!-- Plain Text -->
<mxCell id="unique-id" value="Label Text" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="30" as="geometry" />
</mxCell>

<!-- Bold Title -->
<mxCell id="unique-id" value="Title" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="100" y="20" width="300" height="40" as="geometry" />
</mxCell>

<!-- Multi-line Text (use &#xa; for newlines) -->
<mxCell id="unique-id" value="Line 1&#xa;Line 2&#xa;Line 3" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=10;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="150" height="60" as="geometry" />
</mxCell>
```

## Common Style Properties

### Colors (use hex codes)

| Property | Purpose | Example |
|----------|---------|---------|
| `fillColor` | Background | `fillColor=#dae8fc` |
| `strokeColor` | Border | `strokeColor=#6c8ebf` |
| `fontColor` | Text | `fontColor=#333333` |

### Standard Color Palette

```
Blue:    fillColor=#dae8fc;strokeColor=#6c8ebf
Green:   fillColor=#d5e8d4;strokeColor=#82b366
Yellow:  fillColor=#fff2cc;strokeColor=#d6b656
Orange:  fillColor=#ffe6cc;strokeColor=#d79b00
Red:     fillColor=#f8cecc;strokeColor=#b85450
Purple:  fillColor=#e1d5e7;strokeColor=#9673a6
Grey:    fillColor=#f5f5f5;strokeColor=#666666
```

### Typography

| Property | Values | Example |
|----------|--------|---------|
| `fontSize` | Number | `fontSize=12` |
| `fontStyle` | 0=normal, 1=bold, 2=italic, 3=bold+italic | `fontStyle=1` |
| `align` | left, center, right | `align=center` |
| `verticalAlign` | top, middle, bottom | `verticalAlign=middle` |

### Borders & Effects

| Property | Values | Example |
|----------|--------|---------|
| `rounded` | 0 or 1 | `rounded=1` |
| `strokeWidth` | Number | `strokeWidth=2` |
| `dashed` | 0 or 1 | `dashed=1` |
| `dashPattern` | Pattern | `dashPattern=8 8` |
| `shadow` | 0 or 1 | `shadow=1` |

## Company Branding (Customisable)

This skill supports company-specific branding. Edit `references/branding.md` to set your organisation's colours and styles.

**Default brand placeholders (replace with your own):**
```
Primary:   fillColor=#0066CC;strokeColor=#0052a3;fontColor=#FFFFFF
Secondary: fillColor=#FFB800;strokeColor=#cc9400;fontColor=#333333
Dark:      fillColor=#1a1a2e;strokeColor=#1a1a2e;fontColor=#FFFFFF
Light BG:  fillColor=#f0f4f8;strokeColor=#0066CC
```

See `references/branding.md` for full customisation instructions.

## Templates

Four ready-to-use templates are in `templates/`. Copy and customise — all follow the patterns documented above.

| File | Diagram type | Key patterns used |
|---|---|---|
| `c4-context.drawio` | C4 Context — actors, system boundary, external systems | `mxgraph.c4.person2` shapes, annotation notes, orthogonal edges |
| `microservice-containers.drawio` | C4 Containers — API gateway, services, message bus, databases | Rectangle+badge, annotation notes, fan-out edges, label offset |
| `data-flow.drawio` | Data flow — sync (top row) + async (bottom row) | Lane separators, explicit waypoints, jump arcs |
| `azure-cloud.drawio` | Azure cloud topology — VNet, compute, data, managed services | Image-based azure2 icons, `value=""` + combined child label, fanned + waypoint edges |

## Diagram Patterns

### Architecture Diagram Layout

1. **Title bar** at top (full width, branded color)
2. **Main sections** as swimlanes or rounded containers
3. **Components** as rounded rectangles inside sections
4. **Databases** as cylinders
5. **External systems** on left/right edges
6. **Arrows** showing data/control flow
7. **Legend** in corner explaining colors/symbols
8. **Footer** with metadata

### Component Spacing Rules

**Minimum horizontal gap between a shape and the shape it connects to must be at least 140px.**

This ensures edge labels have enough horizontal run to render above the line without encroaching on either shape. At `fontSize=10`, a typical label like "INSERT / SELECT" or "SQL / Dapper" is ~90–110px wide; 140px gives ~15–25px clearance on each side.

| Connected pair | Minimum gap |
|---|---|
| Service → its database (direct horizontal edge) | 140px |
| Service → Message Bus / Cache | 140px |
| Gateway → first service | 120px (shorter labels like "HTTP") |
| Service → service (routes via waypoints, not direct) | Can be tighter — label is on the routed segment above/below shapes |

**Calculating gap:** `gap = target.x − (source.x + source.width)`.

Example — Service A (x=340, w=150) → DB A (x=630, w=100): gap = 630 − 490 = **140px** ✓

**When to use waypoints instead of increasing gap:**
If two services need a direct label-bearing edge but overlap prevention would push shapes too far right, route the edge above or below (via `exitY=0;entryY=0` with an `Array as="points"` above all shapes) and place the label on the overhead segment. This avoids blowing out the page width.

### Legend Spacing Rules

Space legend rows **22–26 px apart** (measuring from the top of one row to the top of the next). Never share the same `y` value between two separate cells.

**Vertical legend (C4 Context pattern):**
```
legend-bg:  y=T,  height = 8 + 18 (title) + N×24 (rows) + 8 = ~140px for 4 rows
title:      y = T + 6
row 1 box:  y = T + 28   (28px box centres at y+42)
row 1 lbl:  y = T + 33   (vertically aligned with box centre)
row 2 box:  y = T + 56   (22px gap after row 1 ends — row 1 box is 28px tall → ends T+56)
row 2 lbl:  y = T + 58
row 3+:     continue at +24 increments
note:       y = T + last_row_top + 24
```

**Horizontal legend (single row):** all items at the same `y`, spaced ~140px apart along the x axis. Background height ≥ 70px (title row + item row + 8px padding each side).

**Rule**: always check that `item_y + item_height < legend_bg_y + legend_bg_height` — if an item overflows the background, increase `height` on `legend-bg`.

### Layered Architecture (Top to Bottom)

```
┌─────────────────────────────────────┐
│           Users / Clients           │  ← Top layer
├─────────────────────────────────────┤
│           API / Interface           │
├─────────────────────────────────────┤
│         Business Logic              │
├─────────────────────────────────────┤
│         Data / Storage              │  ← Bottom layer
└─────────────────────────────────────┘
```

### Left-to-Right Flow

```
┌──────┐     ┌──────────┐     ┌──────────┐
│Source│ ──► │ Process  │ ──► │  Target  │
└──────┘     └──────────┘     └──────────┘
```

## Best Practices

1. **Unique IDs**: Every mxCell needs a unique `id` attribute
2. **Parent hierarchy**: Set `parent="1"` for top-level elements
3. **Positioning**: Use `mxGeometry` with x, y, width, height
4. **Layering**: Elements defined later appear on top
5. **Alignment**: Use consistent x/y spacing (grid of 10-20px)
6. **Colors**: Use coordinated fill/stroke pairs from the palette
7. **Labels**: Keep text concise; use separate text elements for descriptions
8. **Whitespace**: Leave margins inside containers (20-40px padding)

## Workflow

1. Determine diagram type and layout pattern
2. Set page dimensions in `mxGraphModel` (pageWidth, pageHeight)
3. Create container structure (swimlanes, groups)
4. Add components with unique IDs
5. Add connectors referencing source/target IDs
6. Add labels and annotations
7. Add legend if using color coding
8. Write source as `<name>.drawio` (temporary — used only for the export step)
9. Run the Docker batch export (wraps, exports, sets white background, renames to `.drawio.svg`)
10. Delete the temporary `.drawio` file — only commit the `.drawio.svg`
11. Embed in markdown: `![Title](diagrams/<name>.drawio.svg)`

## Cloud Provider Icons (AWS, Azure, GCP)

Draw.io includes built-in shape libraries for major cloud providers. Use official icons for professional architecture diagrams.

### AWS Icons (Quick Reference)

AWS uses `shape=mxgraph.aws4.resourceIcon` with `resIcon=mxgraph.aws4.SERVICE`:

```xml
<mxCell id="lambda-1" value="Lambda" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="78" height="78" as="geometry" />
</mxCell>
```

**Common AWS resIcon values:**
- Compute: `ec2`, `lambda`, `ecs`, `eks`, `fargate`
- Storage: `s3`, `elastic_block_store`, `elastic_file_system`
- Database: `rds`, `dynamodb`, `aurora`, `elasticache`, `redshift`
- Networking: `vpc`, `cloudfront`, `route_53`, `api_gateway`, `elastic_load_balancing`
- Security: `iam`, `cognito`, `secrets_manager`, `kms`, `waf`

**AWS Category Colors:**
- Compute: `#ED7100`
- Storage: `#7AA116`
- Database: `#C925D1`
- Networking: `#8C4FFF`
- Security: `#DD344C`

### Azure Icons (Quick Reference)

Azure uses `image=img/lib/azure2/CATEGORY/SERVICE.svg`:

```xml
<mxCell id="vm-1" value="VM" style="aspect=fixed;html=1;points=[];align=center;image;fontSize=12;image=img/lib/azure2/compute/Virtual_Machine.svg;verticalLabelPosition=bottom;verticalAlign=top;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="68" height="68" as="geometry" />
</mxCell>
```

**Common Azure image paths:**
- `compute/Virtual_Machine.svg`, `compute/Function_Apps.svg`
- `containers/Kubernetes_Services.svg`
- `storage/Storage_Accounts.svg`, `storage/Blob_Storage.svg`
- `databases/SQL_Database.svg`, `databases/Azure_Cosmos_DB.svg`
- `networking/Virtual_Networks.svg`, `networking/Load_Balancers.svg`
- `security/Key_Vaults.svg`, `identity/Azure_Active_Directory.svg`

### AWS Group Containers

```xml
<!-- VPC -->
<mxCell id="vpc" value="VPC" style="sketch=0;outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;dashed=0;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="400" height="300" as="geometry" />
</mxCell>

<!-- Public Subnet -->
grIcon=mxgraph.aws4.group_public_subnet;strokeColor=#7AA116;fillColor=#E9F3E6

<!-- Private Subnet -->
grIcon=mxgraph.aws4.group_private_subnet;strokeColor=#00A4A6;fillColor=#E6F6F7
```

## References

For advanced patterns and complete icon lists, see:
- `references/architecture-patterns.md` - Common architecture diagram layouts
- `references/style-guide.md` - Extended styling options and icon placement
- `references/cloud-icons.md` - Complete AWS, Azure, GCP icon reference
- `references/branding.md` - Company branding customisation guide
