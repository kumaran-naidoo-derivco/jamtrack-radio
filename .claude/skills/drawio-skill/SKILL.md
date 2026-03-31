---
name: drawio
description: Create and edit draw.io diagram files for architecture diagrams, flowcharts, network diagrams, and technical illustrations. Use when the user asks to create diagrams, architecture visuals, flowcharts, wireframes, network topology, or any visual that should be editable in draw.io/diagrams.net. Outputs .drawio source files and .drawio.svg embedded SVGs for inline GitHub rendering.
---

# Draw.io Diagram Skill

Create professional, editable diagram files in draw.io's native XML format.

## File Format Standard

Every diagram produces **two files**:

| File | Purpose |
|------|---------|
| `<name>.drawio` | Source — XML edited in VS Code or draw.io app |
| `<name>.drawio.svg` | Output — SVG with embedded XML + dark mode CSS, renders in GitHub and VS Code |

The `.drawio.svg` has the draw.io XML embedded (editable in VS Code's draw.io extension) and a CSS `filter` injected that automatically adapts to the viewer's colour scheme — one file, no duplication.

The SVG is exported with an explicit white background so it renders as a self-contained diagram in any context — VS Code dark mode, GitHub light mode, browser. No CSS tricks needed.

**Embedding in markdown:**
```markdown
![Diagram title](diagrams/name.drawio.svg)

> _Edit: open [`name.drawio`](diagrams/name.drawio) in VS Code with the Draw.io Integration extension, then re-export as `.drawio.svg`._
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
         image=img/lib/azure2/networking/Application_Gateway.svg;"
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

| Service | Path |
|---------|------|
| Application Gateway | `networking/Application_Gateway.svg` |
| Kubernetes (AKS) | `containers/Kubernetes_Services.svg` |
| PostgreSQL Flexible Server | `databases/Azure_Database_PostgreSQL_Server.svg` |
| Redis Cache | `databases/Azure_Cache_for_Redis.svg` |
| Blob Storage | `storage/Blob_Storage.svg` |
| Key Vault | `security/Key_Vaults.svg` |
| Entra ID / Azure AD | `identity/Azure_Active_Directory.svg` |
| Log Analytics | `manage_monitor/Log_Analytics_Workspaces.svg` |
| Service Bus | `integration/Service_Bus.svg` |
| Container Registry | `containers/Container_Registries.svg` |

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

```xml
<!-- Basic Arrow -->
<mxCell id="unique-id" value="" style="endArrow=classic;html=1;rounded=0;strokeWidth=2;strokeColor=#666666;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Bidirectional Arrow -->
<mxCell id="unique-id" value="" style="endArrow=classic;startArrow=classic;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="200" as="sourcePoint" />
    <mxPoint x="400" y="200" as="targetPoint" />
  </mxGeometry>
</mxCell>

<!-- Flex Arrow (Block Arrow) -->
<mxCell id="unique-id" value="" style="shape=flexArrow;endArrow=classic;html=1;fillColor=#FFB800;strokeColor=#cc9400;width=20;endSize=8;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="200" as="sourcePoint" />
    <mxPoint x="400" y="200" as="targetPoint" />
  </mxGeometry>
</mxCell>

<!-- Dashed Line -->
<mxCell id="unique-id" value="" style="endArrow=classic;html=1;dashed=1;dashPattern=8 8;strokeColor=#999999;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="200" as="sourcePoint" />
    <mxPoint x="400" y="200" as="targetPoint" />
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
8. Write source as `<name>.drawio` (mxfile XML)
9. Export using the Docker batch export command above (wraps, exports, injects dark mode CSS)
10. Embed in markdown: `![Title](diagrams/<name>.drawio.svg)`
11. Commit both files: `.drawio` (source) and `.drawio.svg` (output)

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
