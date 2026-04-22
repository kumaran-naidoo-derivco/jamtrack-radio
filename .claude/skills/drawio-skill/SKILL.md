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
FILES=(diagram-a diagram-b diagram-c)  # one entry per .drawio file in your folder, no extension

# Step 1 — Ensure <mxfile> wrapper (needed if file starts with bare <mxGraphModel>)
python3 << 'PYEOF'
import os, uuid
diagrams_dir = "<absolute-path-to-diagrams-folder>"
files = ["diagram-a", "diagram-b", "diagram-c"]  # one entry per .drawio file in your folder
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
<mxCell id="svc-hub" value="&lt;b&gt;Hub Service&lt;/b&gt;&lt;br&gt;&lt;&lt;component&gt;&gt;&lt;br&gt;Framework · runtime"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
         verticalAlign=middle;align=center;fontSize=11;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="80" as="geometry" />
</mxCell>

<!-- Azure icon badge — top-right corner, non-interactive -->
<mxCell id="svc-hub_icon" value=""
  style="aspect=fixed;html=1;align=center;image;pointerEvents=0;
         image=img/lib/azure2/networking/Application_Gateways.svg;"
  vertex="1" parent="svc-hub">
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

> ⚠️ **Anti-patterns — never do these:**
> - **Never use `shape=mxgraph.azure2.*` styles with an embedded `value="<b>Label</b>"`** — the stencil renderer and the draw.io label renderer conflict: labels get a white background box and overflow the 75px shape bounds. Use the *rounded rectangle + badge icon* pattern or the *image icon + child label* pattern documented above.
> - **Never set `labelBackgroundColor=#ffffff`** on any cell (shape or edge). It creates an opaque white box over the diagram. Omit `labelBackgroundColor` entirely, or set `labelBackgroundColor=none` on edges.
> - **Blob/Storage icon path is `storage/Storage_Accounts.svg`** — not `Blob_Storage.svg` (that path does not exist in the azure2 library and renders as a broken/missing icon).
> - **Dapr Pub/Sub**: use `integration/Service_Bus.svg` — no native Dapr icon exists in the azure2 library; Azure Service Bus is the closest match.

---

### Component with Annotation Note (preferred pattern for multi-line labels)

When a component label contains more than 2 lines of detail, the text overflows the shape bounds and renders as a floating white box. The fix is a two-part pattern: the **shape label** carries only the service name + stereotype (1–2 lines, always fits), and a **child annotation note** carries the implementation detail as small grey text just below the shape. The child automatically moves with the parent — the same mechanism as the Azure icon badge.

```xml
<!-- Main shape — title + stereotype only (fits cleanly inside box) -->
<mxCell id="svc-hub" value="&lt;b&gt;Hub Service&lt;/b&gt;&lt;br&gt;&lt;&lt;component&gt;&gt;"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
         verticalAlign=middle;align=center;fontSize=11;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="60" as="geometry" />
</mxCell>

<!-- Annotation note — child of svc-hub, auto-moves with parent
     x=0       keeps same left edge as parent
     y=height+4  positions 4 px below the shape bottom
     width=parentWidth  aligns annotation to parent width -->
<mxCell id="svc-hub_note" value="Implementation detail · framework · runtime"
  style="text;html=1;strokeColor=none;fillColor=none;align=center;
         verticalAlign=top;whiteSpace=wrap;fontSize=9;fontColor=#666666;"
  vertex="1" parent="svc-hub">
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

> **Routing rule**: Always include `edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;jumpStyle=arc;jumpSize=10` on every connector. This routes lines in right-angle segments that navigate *around* shapes rather than through them, AND renders a small arc ("jump") wherever one edge crosses another so the two lines stay visually distinguishable. Add explicit `exitX/exitY/entryX/entryY` when auto-routing still crosses a shape.
>
> **Why `jumpStyle` matters**: in any non-trivial diagram, orthogonal edges *will* cross each other at some point. Without a jump style, two crossing lines fuse into a `+` shape at the intersection and the reader cannot tell which segments belong to which edge. `jumpStyle=arc;jumpSize=10` draws a 10px semicircular hop where each crossing occurs — the top line clearly arcs over the bottom one.

```xml
<!-- Basic Arrow (default — use for all connectors) -->
<mxCell id="unique-id" value="label" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;jumpStyle=arc;jumpSize=10;endArrow=block;endFill=1;html=1;rounded=0;strokeWidth=1.5;strokeColor=#555555;fontColor=#444444;fontSize=10;labelBackgroundColor=none;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Bidirectional Arrow -->
<mxCell id="unique-id" value="label" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;jumpStyle=arc;jumpSize=10;endArrow=block;endFill=1;startArrow=block;startFill=1;html=1;rounded=0;strokeWidth=1.5;strokeColor=#555555;labelBackgroundColor=none;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Dashed Line (async / optional dependency) -->
<mxCell id="unique-id" value="label" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;jumpStyle=arc;jumpSize=10;endArrow=block;endFill=1;html=1;dashed=1;dashPattern=8 8;strokeColor=#999999;fontColor=#444444;fontSize=10;labelBackgroundColor=none;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Flex Arrow (Block Arrow — emphasis / bulk data) -->
<mxCell id="unique-id" value="" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;jumpStyle=arc;jumpSize=10;shape=flexArrow;endArrow=block;html=1;fillColor=#FFB800;strokeColor=#cc9400;width=20;endSize=8;labelBackgroundColor=none;" edge="1" parent="1" source="source-id" target="target-id">
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
<!-- ✗ All three overlap at exitY=0.5 of the source -->
<mxCell id="e-gw-a" ... style="...exitX=1;exitY=0.5;..." source="svc-hub" target="svc-a" />
<mxCell id="e-gw-b" ... style="...exitX=1;exitY=0.5;..." source="svc-hub" target="svc-b" />
<mxCell id="e-gw-c" ... style="...exitX=1;exitY=0.5;..." source="svc-hub" target="svc-c" />

<!-- ✓ Fanned out — each edge has its own exit point on the right face -->
<mxCell id="e-gw-a" ... style="...exitX=1;exitY=0.25;entryX=0;entryY=0.5;..." source="svc-hub" target="svc-a" />
<mxCell id="e-gw-b" ... style="...exitX=1;exitY=0.5;entryX=0;entryY=0.5;..." source="svc-hub" target="svc-b" />
<mxCell id="e-gw-c" ... style="...exitX=1;exitY=0.75;entryX=0;entryY=0.5;..." source="svc-hub" target="svc-c" />
```

**Edge label positioning — preventing labels from landing on shapes**: By default, draw.io places the edge label at the geometric midpoint of the routed line. If that midpoint falls over a shape, the label renders on top of the box. Fix with `<mxPoint as="offset">` inside the geometry — it shifts the label in absolute pixels from its calculated position. A negative `y` lifts the label above the line; positive pushes it below.

```xml
<!-- Label shifted 14px above the midpoint — clears any shape underneath -->
<mxCell id="e-svcb-bus" value="publish"
  style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;jumpStyle=arc;jumpSize=10;
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
- **Converging edge label overlap**: when multiple edges from the same node fan out to targets at similar x positions, `y="-14"` alone is not enough — all labels land at similar coordinates. Fix by varying the `x` offset: `x="-40"` pulls the label toward the source, `x="0"` centres it, `x="40"` pushes it toward the target. Combine with `exitY` fan-out so each edge departs from a distinct point on the face.

**Exit face selection — lines must never cross shapes**: Choose `exitX/exitY` and `entryX/entryY` based on the relative position of the target so the line travels directly without backtracking through an obstacle:

| Target is... | Use | Avoid |
|---|---|---|
| Directly below | `exitY=1` (bottom), `entryY=0` (top) | Exiting from top or right |
| Directly above | `exitY=0`, `entryY=1` | Exiting from bottom |
| To the right | `exitX=1`, `entryX=0` | Exiting from left |
| To the left | `exitX=0`, `entryX=1` | Exiting from right |
| Diagonal (down-right) | `exitX=1;exitY=1` (bottom-right corner) | Centre-bottom then sharp turn |

If the direct path crosses an intermediate shape, exit from a **different face** and use waypoints to navigate a clear corridor. Compute waypoints against the bounding boxes of all shapes in the path and stay at least 10px outside any bbox.

**Routing around an intermediate shape — staircase and L-route patterns:**

```
Shared-bus fan-out (preferred when all N edges are unlabeled):
  All edges share the same exit point AND the same horizontal bus y value.
  Lines overlap perfectly on the bus; each branches down to its target at
  its own x. Renders as a single trunk with hanging branches.

  Hub shape bottom-centre at (Cx, Cy); N targets on the row below
  with top-centre x values X1, X2, … XN; pick bus y in the gap between
  Cy and target-top (e.g. (Cy + target_top) / 2):
    every edge: exitX=0.5; exitY=1; entryX=0.5; entryY=0;
                waypoints (Cx, BusY), (Xi, BusY)

  Only use staircase (below) when edges carry distinct labels that must be
  visually separated, or when the bus y would otherwise force labels to
  stack.

Staircase fan-out (use when edges are labeled so each needs its own segment):
  All edges share the same bottom-centre exit on the source shape (Cx, Cy).
  Each turns at its own intermediate y level before heading to its target.
  Stagger y levels by ~6px so segments never share space and labels don't
  collide.

  Hub shape bottom-centre at (Cx, Cy); N targets on the row below
  with top-centre x values X1, X2, … XN:
    edge i (1-based): exitX=0.5; exitY=1; entryX=0.5; entryY=0;
                      waypoints (Cx, Cy + 6·i), (Xi, Cy + 6·i)

L-route (source must bypass an intermediate obstacle to reach target):
  NOTE: if the obstacle is a sibling container (namespace, zone, swimlane)
  rather than a load-bearing vertex shape, FIRST try moving the container
  (see Rule 7). L-routing around a container that should have been moved
  produces unnecessary waypoints and reads as a design smell. Use L-route
  only when the obstacle genuinely cannot be relocated.

  Exit from the face away from the obstacle → travel along a safe corridor
  just outside the obstacle's bbox → turn and approach the target from a
  clear face.

  Source right face at x = R; target is below and to the right; an
  intermediate obstacle has bbox [Ox1 – Ox2, Oy1 – Oy2]:
    exitX=1; exitY=0.5  (exit source right face)
    WP1  (Ox2 + 20,  Oy2 + 40)   ← vertical corridor, 20px past obstacle right
    WP2  (Tx,        Oy2 + 40)   ← horizontal run, 40px below obstacle bottom
    entry (Tx, Ty)               ← clear top/left entry on target

N-lane corridor (fan-out from one source to a COLUMN of N targets):
  The dual of staircase fan-out: where staircase distributes N edges across
  staggered y levels into a row of targets, the corridor distributes them
  across staggered x levels into a column of targets.

  Source right face at x = R; N targets stacked vertically, each with left-
  centre at (Tx, Yi). Pick N nearby x values L1 < L2 < … < LN (5–6px apart)
  for each edge's vertical segment, so the vertical runs never overlap:

  For edge i (1-based), with target left-centre (Tx, Yi):
    exitX=1; exitY=yi          (stagger source exits so starts don't overlap)
    entryX=0; entryY=0.5
    waypoints (Li, Yexit_i), (Li, Yi)

  Example with 4 targets and L1..L4 = R+10, R+16, R+22, R+28:
    edge 1 → target at Y1:  WPs (L1, Yexit_1), (L1, Y1)
    edge 2 → target at Y2:  WPs (L2, Yexit_2), (L2, Y2)
    edge 3 → target at Y3:  WPs (L3, Yexit_3), (L3, Y3)
    edge 4 → target at Y4:  WPs (L4, Yexit_4), (L4, Y4)

  Use this when targets have DIFFERENT labels. When all N edges share the
  SAME label, bundle them instead (see Rule 2aa) — a corridor with four
  identical labels is visual noise.
```

> ⚠️ **Never rely on auto-routing to avoid shape crossings.** draw.io's orthogonal router routes around container group cells but it does NOT detect vertex shapes as obstacles — it will happily draw a straight line through an icon or a service box. Always trace the path manually and add waypoints when any segment intersects a vertex shape's bounding box.

When auto-routing still crosses a shape, add explicit waypoints to route around it:

```xml
<mxCell id="e3" value="label" style="edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;jumpStyle=arc;jumpSize=10;exitX=0.5;exitY=0;entryX=0.5;entryY=0;endArrow=block;endFill=1;html=1;strokeColor=#555555;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="200" y="100" />  <!-- waypoint above the obstructing shape -->
      <mxPoint x="500" y="100" />
    </Array>
  </mxGeometry>
</mxCell>
```

## Layout & Spacing Rules

> These rules apply to every new diagram and every edit. The most common cause of an unreadable diagram is not the shapes or the edges but the **spacing** — layouts designed against shape bounding boxes instead of their rendered visual footprints look "squashed" no matter how carefully the edges are routed. Always size canvases, containers, and gaps against the rules below.

### Rule 1 — Effective visual footprint

A shape's *bounding box* (the `w × h` on its `mxGeometry`) is NOT the same as its *visual footprint* (the space it occupies on the rendered canvas, including child labels, notes, and badge icons).

| Pattern | Bbox | Visual footprint | Notes |
|---|---|---|---|
| Plain rounded rectangle (label inside) | `w × h` | `w × h` | Self-contained — use the bbox directly |
| Rounded rect + badge icon + inline note | `w × h` | `w × h` | Notes merged inside via HTML `<br>` — self-contained |
| Image icon + child label at `(-28, 68, 130, 36)` | `75 × 65` | `~130 × 104` | Label extends 28px left, 55px right; extends ~39px below the icon bottom |

Always plan layouts against the **visual footprint**, not the bbox. For image icons, reserve 40px below the icon for the label tail, and allow the 130px label to overflow ~28px left and ~27.5px right of the icon column.

### Rule 2 — Minimum row / column pitch

**Row pitch** = vertical distance between successive rows (top of row A → top of row B).

| Row content | Min pitch |
|---|---|
| Plain rectangles, no edge labels between rows | row height + 50 |
| Plain rectangles, labeled edges between rows | row height + 80 |
| Image icons + child labels (rendered height ~104) | 160 |
| Image icons + labels + labeled edges between rows | 200 |

**Column pitch** = horizontal distance between successive shapes in the same row.

| Column content | Min pitch |
|---|---|
| Plain rectangles, no edge labels | shape width + 40 |
| Plain rectangles, labeled edge between them | shape width + max(120, label width + 40) |
| Image icons (75w) with 130w labels | 170 (gives ~20px clearance between label boxes) |

### Rule 2a — Shapes per row (structural readability)

A diagram with more than **4 shapes on the same row** at standard sizes (150–200px wide) gets cramped fast, because every horizontal gap now has to hold an edge label. At 5+ shapes per row, label overflow onto adjacent shapes becomes unavoidable without either shrinking the shapes (which hurts readability) or widening the canvas to an unreasonable size.

> Prefer **stacking onto extra rows** over packing one row tightly. Let the canvas grow vertically — canvas size is free, but overlapping labels are not. If a flow has 5+ shapes, split into two parallel rows (e.g. "source domain" on top, "target domain" on bottom, event bus between them) rather than a single wide row.

### Rule 2aa — Bundle identical-label edges from one source

When a single source shape has multiple edges with the **same label** going to different targets (e.g. three "Managed Identity" connections from one service to three Azure resources), do NOT draw three near-parallel lines with three copies of the same label — it reads as clutter and the lines crowd each other.

Instead, **bundle** them: all edges share the same exit point on the source AND the same first waypoint, so they visually merge into a single trunk before branching to each target. Put the label on only ONE of the edges; remove (`value=""`) it from the others.

```
Source shape with right face at x=R, bundled trunk endpoint at (T, Ymid):

  Edge 1 (carries label):  exit (R, Ymid) → waypoint (T, Ymid) → waypoint (T, Y1) → entry target-1
  Edge 2 (value=""):       exit (R, Ymid) → waypoint (T, Ymid) → waypoint (T, Y2) → entry target-2
  Edge 3 (value=""):       exit (R, Ymid) → waypoint (T, Ymid) → waypoint (T, Y3) → entry target-3

  All three exits are identical → draw.io renders them as one line from source to (T, Ymid).
  After the shared waypoint each edge peels off to its own target.
  Only edge 1 shows the label, positioned by offset toward the shared trunk segment.
```

If the label belongs to *all* edges equally, pick the one whose midpoint lands nearest the shared trunk so the label visually attaches to the bundled line. Use an x-offset (`x="-60"` or similar) to pull the label toward the trunk side of the edge.

### Rule 2b — Parallel edges between the same pair of shapes

When two edges run between the same source and target (e.g. an INSERT and a later UPDATE), place them on different exit/entry y values with **enough vertical separation to clear the label rows**.

- Minimum separation: `exitY` values at least 40% apart (e.g. `0.25` and `0.75`, not `0.35` and `0.65`)
- Minimum shape height: 100px so that a 40% separation is at least 40px of vertical offset
- Combine with x-offset on each label (`x="-40"` for one, `x="40"` for the other) so labels do not stack vertically on top of each other

If the parallel edges still look cluttered, the two boxes are too close — widen the gap between them.

### Rule 2c — Multi-line labels for long text

An edge label longer than ~15 characters will overflow most horizontal gaps. Use HTML line breaks (`&lt;br&gt;`) to split long labels into two short lines:

| Raw label (33 chars, ~220px) | Multi-line variant (16 chars/line, ~110px wide) |
|---|---|
| `8. subscribe: StorageObjectCreated` | `8. subscribe:<br>StorageObjectCreated` |
| `4. gRPC: Store (blob bytes)` | `4. gRPC: Store<br>(blob bytes)` |
| `9. gRPC: SetStorageRef (async)` | `9. gRPC:<br>SetStorageRef (async)` |

Multi-line labels are twice as tall (~32px) but half as wide. In a vertical edge they fit alongside a short vertical segment; in a horizontal edge they fit inside a narrower gap.

### Rule 3 — Container sizing

A container (subnet, zone, system boundary, swimlane) must be sized to hold the **visual footprints** of its children plus padding, not just their bboxes.

Formula: `container.h ≥ Σ(child visual heights) + (n+1) × 25px vertical padding`

For a zone or subnet holding a single row of 75×65 icons with labels:

```
min height = 30  (zone title area)
           + 20  (top padding)
           + 65  (icon)
           +  3  (gap)
           + 36  (child label)
           + 25  (bottom padding)
           = 179px — round to 180px
```

For a stack of 4 such zones: total height ≥ 4 × 180 + 3 × 20 (inter-zone gap) = 780px before adding the outer title row.

### Rule 4 — Edge label gap

An edge label renders at the geometric midpoint of the routed line by default. If the label is longer than the segment it lands on, it visually overflows onto adjacent shapes.

Before placing a label:

- Estimate rendered width: at 10pt, `len(text) × 6.5 + 10` pixels is a close upper bound.
- The segment the label falls on must be **≥ label width + 20px clearance**.

When the segment is too short, fixes in order of preference:

1. **Widen the source/target gap in the layout** (preferred) — the label content is the user-chosen description and should stay as the author wrote it. Move shapes apart so the label fits.
2. **Move the label onto a longer segment** via `<mxPoint as="offset" x="...">` — useful when the edge has multiple segments and one is long enough.
3. **Split to two lines** with `&lt;br&gt;` (Rule 2c) — halves the width at the cost of doubling the height. Use when widening isn't possible (e.g. fixed container).
4. **Shorten the label** (last resort) — loses information; only acceptable for labels like `3. INSERT track (storage_ref=NULL)` → `3. INSERT track` where the trailing detail duplicates something the reader can infer.

**Worked example (abstract):** a 33-character label like `N. VERB resource (detail=value)` renders at ~225px. An edge whose shortest segment is only 80px cannot hold it. Widen the segment to ≥ 250px by moving source and target apart — that is the preferred fix.

### Rule 5 — Canvas sizing (shapes drive the canvas, not vice versa)

The canvas is an **output** of the layout, not an input. Lay out shapes with proper spacing first (Rules 1–4), then size the canvas to contain them with 30–50px margin on all sides.

```
canvas_width  = (rightmost_edge + right_label_overflow)
              - (leftmost_edge  - left_label_overflow)
              + 80px total margin
```

Do NOT start from a predetermined canvas size (e.g. "let's fit this in 1200×800") and squeeze shapes to fit. If the layout needs 1800×1000 to be readable, the canvas is 1800×1000. A compressed canvas is the #1 cause of the "squashed" complaint.

> **When in doubt, err generous.** Empty canvas is free; cramped shapes are not. It's always easier to trim unused margin later than to rescue a design that started too cramped.

### Rule 5a — Shape size must fit its label content

A rectangle's width and height must be big enough to render its label text without truncation or wrapping artifacts.

Rough sizing at `fontSize=11` (default):

| Label content | Min width | Min height |
|---|---|---|
| 1 line, ≤15 chars | 120 | 40 |
| 1 line, 16–25 chars | 180 | 40 |
| 2 lines (title + stereotype) | 140 | 60 |
| 3 lines (title + stereotype + grey note) | 160 | 90 |
| 4 lines (pod name + role + port + framework) | 110 | 90 (compact stack) |

A deployment-pod label like `<b>Service Name</b><br>Role :PORT` on two lines needs at least ~110px width to avoid awkward character truncation. A 60×60 pod is too small — use 100×80 minimum.

> If the label does not fit at the chosen shape size, EITHER grow the shape OR shorten the label — never let the rendered text overflow the shape bounds.

### Rule 6 — Nested shape positioning

Shapes inside containers must be positioned so their **visual footprint** stays inside the container, with padding.

For a child at relative `(x, y)` with visual footprint `w × h`:

- `x ≥ 20` (left padding)
- `x + w ≤ container.width − 20` (right padding)
- `y ≥ 30` (top padding — space for container title)
- `y + h ≤ container.height − 20` (bottom padding)

For image-icon children the visual footprint extends 39px below the icon bbox and 28px to its left / 27.5px to its right; check those extremes, not just the icon bbox.

In rows of multiple nested shapes, distribute x positions so `Σ(visual widths) + Σ(gaps) ≤ container inner width`.

> **Cross-reference**: the fan-out rule and exit-face selection above are edge-routing concerns. They assume the underlying layout already respects the spacing rules on this page. If a diagram feels crowded *despite* correct routing, the fix is almost always here — widen rows, columns, or the canvas itself.

### Rule 7 — Sibling containers must not block primary edge corridors

When a primary shape inside a subnet/zone (e.g. a central service pod, an API gateway) has edges to targets outside that subnet, those edges travel through a **corridor** — the spatial region between the primary shape and the boundary of its parent container. Do NOT place *other* sibling containers (secondary namespaces, environment boxes, metadata swimlanes) inside this corridor — they force every edge to re-route around them.

**Symptom**: edges cross through a secondary container shape, or need 3+ waypoints just to escape the enclosing subnet.

**Fix**: move the blocking container, not the edges. Two structural patterns work:

1. **Vertical stacking** — stack all sibling containers full-width of the parent, one above the other. The left and right edges of every stacked container are clear, so the corridor opens up on both sides.
2. **Edge-of-parent anchoring** — put secondary containers flush against one edge of the parent (top or bottom). Leave the opposite edge free as the corridor.

```
✗ Anti-pattern — ns_staging blocks the corridor:

  aks_subnet ┌────────────────────────────────────────┐
             │ ns_prod [pods]            ns_staging   │
             │  ┌──────────────────┐     ┌─────────┐  │
             │  │ apigw ── 3 edges ┼─────┼ XXXXXXX │  │ ← edges cross ns_staging
             │  └──────────────────┘     └─────────┘  │
             │                           ns_system    │
             │                           ┌─────────┐  │
             │                           │ XXXXXXX │  │
             │                           └─────────┘  │
             └────────────────────────────────────────┘

✓ Vertical stacking — corridor clear:

  aks_subnet ┌────────────────────────────────────────┐
             │ ns_prod (full width)                   │
             │  ┌──────────────────────────────────┐  │
             │  │ apigw ───────── 3 edges ─────────┼──┼──→ right-column targets
             │  │ [pods...]                        │  │
             │  └──────────────────────────────────┘  │
             │ ns_staging (full width, below)         │
             │ ns_system  (full width, below staging) │
             └────────────────────────────────────────┘
```

Only resort to edge re-routing (waypoints above/below the blocking container — the L-route pattern) when the container genuinely cannot be moved. Examples where the container IS load-bearing: zone stacking in a STRIDE trust-boundary diagram (zone order encodes trust gradient), rack layout in a physical diagram (physical position IS the information).

> **Move the container first. Route around only as a last resort.** A diagram whose primary flow is obstructed by secondary containers is mis-laid-out. Fix the layout; don't patch the edges.

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
