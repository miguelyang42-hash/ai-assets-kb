# White Background

## Routing Header

- **Load when**: user asks for pure white (#FFFFFF) background, white-background hero image, or platform/listing image requiring a white background.
- **Do not load when**: user asks for non-white background, lifestyle scene, color background, native crop/resize only, or selling-point layout.
- **Merge notes**: for platform hero, centering, shadow, lighting cleanup, logo placement, or other same-output edits, prefer one merged `simple_generation` prompt instead of chaining `white_background` with additional AI calls.
- **Hard stop**: do not redraw, beautify, recolor, relight, remove labels, or alter product-attached text/logos.

## Scene Description

Replace the image background with pure white (#FFFFFF) while preserving the product subject with sharp edges and full detail integrity.

## Apply Method: Direct Apply

Use the appropriate prompt variant. Do not add creative scene, layout, or marketing content beyond the fixed preservation constraints in this file.

## Routing Modes

| Mode | When to Use | Execution |
|------|-------------|-----------|
| `pure_background_replacement` | User only wants the existing product on pure white | Prefer native background removal/compositing if available; otherwise use `image_edit` + `white_background`. |
| `platform_white_hero` | User asks for platform/listing/main image with white background, centering, coverage, shadow, or final size | Use the platform workflow in `SKILL.md`; this scene supplies the white-background sub-task only. Final resize/format is native. |

Do not use this scene as a one-step solution for multi-image listing sets, SKU batches, selling-point layouts, text edits, or crop/resize/format-only requests.

## Prompt Templates

### Variant A — No brand elements visible on product

```
Replace the background with pure white (#FFFFFF).
CRITICAL: Preserve the product exactly — maintain sharp edges, original colors, textures, surface details, and any text/labels on the product.
Do NOT soften edges, alter product colors, or remove any product-attached elements.
Do NOT generate a new product photo. Do NOT change perspective, product scale, shape, label text, material, lighting on the product surface, or add/remove accessories.
```

### Variant B — Brand logo/text visible on product

```
Replace the background with pure white (#FFFFFF).
CRITICAL: Preserve the product exactly — maintain sharp edges, original colors, textures, surface details, brand logos, and all text/labels on the product.
The brand identity elements (logos, text, tags) are part of the product and must NOT be removed or altered.
Do NOT generate a new product photo. Do NOT change perspective, product scale, shape, label text, material, lighting on the product surface, or add/remove accessories.
```

**Selection rule**: Agent visually inspects the image for brand logos/text on the product. If uncertain, default to Variant B (safer — protects more elements).

## Tool Invocation

- Tool: `image_edit`
- task_type: `white_background`

## Notes

- Product shape, color, texture, material details, and structural features must remain 100% identical to the original
- Product-attached elements (labels, tags, logos, text) are part of the product and must be preserved
- White-background editing must never redraw or "beautify" the product. If the model changes the product, treat the result as failed and retry with a narrower/native approach.
- This scene only handles background replacement to pure white — for watermark removal, use the Watermark Removal scene
- **1:1 aspect ratio only**: if the user requests a non-1:1 ratio, auto-switch to `simple_generation` (see SKILL.md aspect ratio rules). The prompt still follows this scene's template.
- **Single-purpose constraint**: if the request includes 2 or more intents, platform/listing readiness, composition changes, lighting changes, or broad optimization language, use a merged `simple_generation`, merged `complex_generation`, or `true_sequential` plan only when required by SKILL.md Step 4.
