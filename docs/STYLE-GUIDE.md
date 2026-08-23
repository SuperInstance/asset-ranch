# ROBLOX-STYLE PROMPT KIT — STYLE GUIDE v1

Grounded in Roblox devforum low-poly doctrine (Smooth Plastic + bright colors,
devforum.roblox.com/t/278566, /t/235354) and classic stud-era toy aesthetics.
Goal: **readable at distance, kid-bright but coherent, zero photoreal noise.**

## 1. Core Vocabulary (use these words, they carry the style)

- **chunky** — thick proportions, nothing spindly
- **beveled-block** — soft chamfered edges on blocky geometry, like injection-molded plastic
- **saturated / punchy colors** — candy-bright primaries and secondaries
- **flat-lit / soft directional light** — one simple light, no complex shading
- **toylike** — proportions of a toy figurine, oversized features
- **clean silhouette** — the shape reads in one glance, works as a 64px icon
- **smooth plastic material** — the Roblox "Smooth Plastic" feel: uniform matte, no surface grain
- **isometric 3/4 view** — the canonical prop presentation angle
- **solid background** — flat neutral or single-hue backdrop for clean cutouts
- **studs-and-holes DNA** — where it fits, evoke classic brick topology without drawing literal studs unless asked

## 2. Global Style Suffix (append to every positive prompt)

```
chunky beveled-block low-poly 3D render, toylike proportions, saturated
punchy colors, smooth plastic material, flat lighting, clean silhouette,
isometric 3/4 view, solid flat background, game asset, crisp edges
```

## 3. Global Negative Prompt (always)

```
photorealistic, photographic, realistic textures, noise, grain, gritty,
rust overlays, dirt detail, thin spindly parts, fragile wires, hairline
detail that disappears at distance, cinematic depth of field, motion blur,
HDR, harsh shadows, ambient occlusion grime, text, watermark, cluttered
background, complex shading, subsurface scattering
```

Why each ban:
- *photoreal / noise / grit* — the #1 quality killer; Roblox reads clean from across the map
- *spindly detail* — antennas, wires, filigree die at 50 studs distance
- *complex shading* — baked AO/HDRI look fights the flat Roblox lighting model

## 4. Canonical Prompt Templates by Asset Class

### 4.1 Prop
```
{SUBJECT}, {COLOR NOTES}, {MATERIAL: painted metal / smooth plastic},
chunky beveled-block low-poly 3D render, toylike proportions, saturated
punchy colors, flat lighting, clean silhouette, isometric 3/4 view,
solid flat background, game asset
```
Example: `a scrapyard engine block, bright orange block with teal accents and cartoon bolts, painted metal, ...`

### 4.2 Vehicle Part
```
{PART: wheel / bumper / engine}, chunky oversized toy version, {COLOR},
beveled-block low-poly 3D render, smooth plastic material, flat lighting,
clean silhouette, isometric 3/4 view, solid flat background
```

### 4.3 Character Part (torso, head, accessory)
```
{PART} for a blocky avatar, {COLOR}, chunky beveled-block low-poly 3D
render, toylike proportions, smooth plastic material, flat lighting,
front view, solid flat background, game asset
```

### 4.4 Texture / Tile (seamless)
```
seamless tileable texture, {SURFACE: rust plates / hazard stripes / planks},
stylized flat colors, saturated, minimal detail, no lighting, no shadows,
top-down orthographic, repeating pattern, game texture
```
Note: for tiles, ask for *no lighting* — lighting is added by the engine.

### 4.5 Icon (UI)
```
{SUBJECT} icon, simple bold shape, {COLOR}, chunky beveled-block low-poly
style, thick outline-friendly silhouette, flat lighting, centered,
solid flat background, readable at 64x64 pixels, game UI icon
```

### 4.6 Skybox Gradient
```
smooth vertical sky gradient from {TOP COLOR} to {HORIZON COLOR},
flat colors, no clouds unless requested, no noise, seamless, game skybox
```
(Consider generating skyboxes as plain engine gradients first — often better than any image.)

### 4.7 Decal / Sticker
```
{SUBJECT} sticker, bold flat colors, thick clean outlines, sticker die-cut
shape, saturated, no background, no gradient banding, readable at small size
```

### 4.8 Terrain Chunk
```
{BIOME} terrain chunk, stylized low-poly, chunky geometric rocks, saturated
coherent palette, flat lighting, smooth plastic material, no photoreal
detail, isometric 3/4 view, solid background
```

### 4.9 Tool / Held Item
```
{TOOL} held item, chunky toy version, oversized head, short handle, {COLOR},
beveled-block low-poly, smooth plastic, flat lighting, clean silhouette,
3/4 view, solid flat background
```

### 4.10 Signage
```
{SHAPE} sign with {SYMBOL}, bold flat colors, thick border, chunky
beveled-block low-poly, readable at distance, flat lighting, solid background
```

## 5. Palette Discipline

- 3–5 hues per asset; one dominant, one accent, one neutral.
- Coherent > maximum-bright. Pick a campaign palette (e.g. Scrapcraft:
  rust-orange, steel teal, safety-yellow, soot-charcoal, off-white) and stick to it.
- Contrast is legibility: dark silhouettes on light grounds and vice versa.

## 6. Acceptance Check (before sending to review)

1. Squint — is the silhouette still readable? If not: reject.
2. Zoom to 64px — still identifiable? If not: reject.
3. Any photoreal grain or muddy shadows? Reject and strengthen negatives.
4. Does the color sit in the campaign palette? If not: reject.
