# Watermark Removal

## Routing Header

- **Load when**: user asks to remove an authorized watermark, website URL, contact information, QR code, accidental overlay, stain, dust, scanner mark, or non-product visual clutter.
- **Do not load when**: target is product/package text, product brand marks, same-language text replacement, full-image translation, or new marketing copy.
- **Merge notes**: small non-product clutter can often merge into one `simple_generation` call with background/listing cleanup. Dense or ownership-like watermarks may require a separate `watermark_removal` step or rights confirmation.
- **Hard stop**: do not remove third-party ownership marks, platform watermarks, photographer signatures, or copyright marks unless the user confirms rights.

## Scene Description

Remove authorized watermarks, website URLs, contact information, QR codes, accidental overlays, stains, dust, scanner marks, and other non-product visual clutter from the image, while preserving all product-related text and visual elements.

This scene is for non-product overlays only. It is not the default route for deleting specified product/package text.

## Rights and Safety Boundary

Watermark removal is only allowed when the user owns the image or has rights to edit it.

Do not help remove third-party copyright marks, platform watermarks, photographer signatures, or ownership identifiers to bypass licensing.

Allowed cases include removing the user's own watermark, accidental overlays, stains, dust, scanner marks, or non-ownership visual clutter.

## Route Boundary

| Request Type | Route |
|--------------|-------|
| Remove user's own watermark, URL, QR code, contact info, accidental overlay, stain, dust, scanner mark, or non-product clutter | This Watermark Removal scene |
| Remove third-party platform mark, photographer mark, copyright notice, or ownership identifier | Do not proceed unless the user confirms they own the image or have rights to edit it |
| Remove specified product/package text but keep the rest of the layout | Use Text Editing's local text removal flow (`simple_generation` / `complex_generation`) |
| Replace text with new text | Text Editing |
| Translate all visible text | Image Translation |
| Remove text + change background / platform image / resize | Multi-step pipeline |

## Known Limitation

> **Important**: Watermark removal quality varies by runtime and watermark complexity. Some tools redraw text regions instead of cleanly removing them. For complex or dense watermarks, inform the user that results may not be ideal and suggest dedicated watermark removal tools if available.

## Apply Method: Direct Apply

Agent should visually inspect whether the image has a product brand logo in the top-left corner, then select the appropriate variant. If the logo could be an ownership watermark rather than product branding, ask for confirmation before removing or preserving it.

## Prompt Templates

### Variant A — No brand logo in top-left corner

```
Remove only the authorized watermark, website information, contact details, QR code, accidental overlay, stain, dust, scanner mark, or non-product clutter from the image. Preserve product-related text that is visibly present in the ORIGINAL image. IMPORTANT: Keep all product details, colors, textures, and structural features exactly unchanged.
Do not remove or alter any product labels, packaging text, specifications, brand marks that are part of the product, or non-target text.
```

### Variant B — Brand logo present in top-left corner

```
Remove only the authorized watermark, website information, contact details, QR code, accidental overlay, stain, dust, scanner mark, or non-product clutter from the image. Preserve product-related text and the top-left product brand logo that is visibly present in the ORIGINAL image. IMPORTANT: Keep all product details, colors, textures, and structural features exactly unchanged.
Do not remove or alter any product labels, packaging text, specifications, brand marks that are part of the product, or non-target text.
```

## Tool Invocation

- Tool: `image_edit`
- task_type: `watermark_removal`

## Pre-execution Guidance

Before calling the tool, the Agent should:
1. Assess watermark complexity (simple corner watermark vs. dense/full-image overlay)
2. For dense/complex watermarks, proactively inform the user: "The AI watermark removal may have limited effectiveness on complex watermarks. I'll attempt it, but the result may need manual refinement."
3. After execution, if the result is poor (text garbled, watermark partially remaining), suggest the user try a dedicated watermark removal tool

## Notes

- Product-related text (product name, specifications, etc.) must be preserved
- Only remove authorized watermarks, URLs, contact info, QR codes, accidental overlays, stains, dust, scanner marks, and other non-product visual clutter
- Do not use this scene for product/package text removal, product brand removal, or unclear third-party ownership marks
- **1:1 aspect ratio only**: if the user requests a non-1:1 ratio, auto-switch to `simple_generation` (see SKILL.md aspect ratio rules). Prompt still follows this scene's template.
- **Single-purpose constraint**: if the request includes 2 or more intents, platform/listing readiness, composition changes, lighting changes, or broad optimization language, use a merged `simple_generation`, merged `complex_generation`, or `true_sequential` plan only when required by SKILL.md Step 4.
