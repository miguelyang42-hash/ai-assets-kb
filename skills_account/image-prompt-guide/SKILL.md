---
name: image-prompt-guide
description: >-
  Prompt engineering and tool routing for AI image generation and editing.
  Use for: creative generation, product photo editing, e-commerce platform image sets,
  and specialized scenes (white background, authorized watermark/element cleanup, HD upscale, scene swap,
  model showcase, selling point, logo design, tech pack, etc.).
  Do NOT use for: full product development workflows (use ai-product-designer),
  or non-AI operations like resize/crop/compress/format-convert (use native tools).
enabled: true
---

# Image Generation Guide

## Core Rules

| # | Rule | Description |
|---|------|-------------|
| 1 | **No Hallucination** | Do not fabricate product facts, selling points, certifications, dimensions, materials, brand assets, text, labels, hidden details, or unsupported claims. Visual execution choices such as lighting, composition, clean background, natural shadow, camera angle, whitespace, and style may be inferred when they do not change the product meaning or introduce new factual claims. After constructing a prompt, verify that all factual instructions trace back to the user request, visible image evidence, or confirmed platform requirements. |
| 2 | **Clarify Before Guessing** | Ask only for blocking ambiguity: no actionable verb, context-only replies like "yes"/"right" with no prior clear instruction, or folder references without per-image instructions. For safe default ambiguity such as "make it cleaner/professional", proceed with conservative visual cleanup and do not invent factual claims. |
| 3 | **Preserve-First Editing** | When editing, stating what NOT to change is more important than what to change. Every edit prompt must include a preservation clause listing elements that must remain untouched. |
| 4 | **Be Specific** | Define subject, environment, lighting, mood, and style explicitly. Replace vague terms ("beautiful", "professional") with concrete visual descriptors. Use natural sentences for describing intent; comma-separated keywords are acceptable for style/quality modifiers (e.g., "8K, hyperrealistic, sharp detail"). |
| 5 | **Incremental Refinement** | When the user requests a follow-up change to a previous result, apply targeted edits rather than regenerating from scratch. Preserve what already works, fix only what the user calls out. |
| 6 | **No Brand Infringement** | Do not include recognizable brand logos, names, or trademarked elements unless the user explicitly requests their own brand assets. For logo design, see `references/logo-design.md` for detailed anti-infringement rules. |

---

## Reference Loading Contract

References are part of the required workflow, not optional background reading.

Before constructing a prompt, choosing a final `task_type`, or calling any image tool:

1. Match the request to the Scene Router.
2. Load every matched scene reference listed in the router table.
3. For composite workflows, load only the composite reference plus the references for the selected output scenes.
4. Apply the loaded reference's prompt template, hard constraints, safety boundaries, and tool invocation rules.
5. If a request matches multiple scenes for the same output image, read each matched reference, then decide whether to merge them into one call using Step 4.

Do not skip a reference because the router table appears sufficient. The table is only an index; the detailed rules live in `references/`.

**Reference loading index**:

| Matched Scene | Must Load | Do Not Load When |
|---------------|-----------|------------------|
| Platform Product Image | `references/platform-product-guidelines.md` plus each selected output scene reference | User only asks for generic product cleanup with no platform/listing intent |
| White Background | `references/white-background.md` | User wants non-white background, scene swap, or native resize/crop only |
| Watermark / Element Removal | `references/remove-watermark.md` | User wants product/package text replacement/removal, translation, or new marketing copy |
| HD Upscale | `references/hd-upscale.md` | User wants file-size increase, format conversion, or content changes |
| Scene Image | `references/scene-image.md` | User wants pure white background only, product recolor only, or text-only changes |
| SKU Color Change | `references/sku-color-change.md` | User wants background color change rather than product color change |
| Logo Customization | `references/logo-customization.md` | User asks to design a new logo from scratch |
| Model Showcase | `references/model-showcase.md` | User wants model plus new lifestyle scene or selling-point copy; then load Scene Image or Selling Point too |
| Image Detail | `references/image-detail.md` | User wants callouts, annotations, dimensions, or marketing copy |
| Selling Point Image | `references/selling-point.md` | User only wants a local product detail crop without text/layout |
| Image Translation | `references/image-translation.md` | User asks to replace only specified same-language text |
| Text Editing | `references/text-editing.md` | User asks to translate all visible text or add new marketing copy |
| Logo Design | `references/logo-design.md` | User already has a logo and wants it applied to a product |
| Tech Pack | `references/tech-pack.md` | User wants an e-commerce spec infographic rather than production/OEM drawings |
| General Style Enrichment | `references/style-guide.md` | A specialized scene already provides enough prompt detail |

---

## Request Processing Pipeline

Process every request through these steps in order:

### Step 0 — Image Intake

If the user provides one or more images, inspect the image before routing.

Identify:
- Main subject
- Elements that must be preserved
- Visible text, logos, labels, watermarks
- Current aspect ratio
- Quality issues such as blur, low resolution, artifacts, occlusion
- Whether the image appears to be a product photo, poster, document, logo, model photo, or scene photo

Use this intake result to build preservation clauses and choose routing.
Never infer hidden or occluded product details.

### Step 0.5 — Image Edit Source Preflight

Before any `image_edit` call, prepare every reference image:

1. **Read before edit**: inspect the image source and confirm it is reachable, decodable, and image-like. Capture at least format/MIME, dimensions, file size when available, visible content summary, and any quality risks that affect routing.
2. **Local path handling**: if the user provided a local filesystem path, do not pass it directly to `image_edit`. Read and validate the local file first, upload it to the configured CDN or asset host, then use the returned HTTPS URL as the `reference_images` input.
3. **Remote URL handling**: if the user provided an HTTP(S) URL, verify that it can be read as an image before editing.
4. **Fail closed**: if the image cannot be read, decoded, verified, or converted to an HTTPS URL, stop before `image_edit` and report the blocker. Do not guess-edit an unread image or pass `file://` / raw local paths to remote image-edit tools.

When uploading local images, avoid exposing sensitive metadata: strip EXIF/GPS data unless the user explicitly needs it preserved, and do not log signed CDN URLs or private local paths.

### Step 1 — Outcome Intent First

Before choosing any `task_type`, identify the user's desired final outcome.

Classify the request by outcome intent first:

| Intent | Meaning |
|--------|---------|
| `platform_main_image` | Platform-ready hero/main product image |
| `platform_image_set` | Multi-image set for a listing |
| `product_cleanup` | Cleaner, more professional product photo |
| `background_replacement` | Change or replace background |
| `text_removal` | Remove specified text, ownership overlays, or visual clutter with the correct safety route |
| `text_replacement` | Replace or translate text in image |
| `selling_point_image` | Marketing layout with copy/callouts |
| `logo_design` | Create a new logo from scratch |
| `logo_customization` | Apply existing logo to product/material |
| `upscale_or_restore` | Improve clarity/resolution |
| `native_delivery` | Resize, crop, compress, convert format |

`task_type` is only an execution hint. It must not replace outcome-intent analysis.

### Step 2 — Non-AI Task Interception

Before invoking any AI image tool, check whether the request is a non-AI operation. If the user's core intent is to change the image's **size, file weight, format, or orientation** without altering content, route to native (non-AI) tools instead.

| Signal | Action |
|--------|--------|
| Crop / trim / cut to dimensions (not SKU asset creation) | Use crop/resize tool |
| Compress / reduce file size / "under X MB" | Use compress tool |
| Resize to WxH / change dimensions | Use resize tool |
| Format convert (PNG/JPG/WebP) | Use format_convert tool |
| Rotate / flip | Use transform tool |

**Key indicator**: phrases like "keep everything else unchanged", "just resize", explicit pixel dimensions with no content change, or file-size constraints ("under 2MB") strongly signal non-AI tasks.

SKU-related requests such as "split into SKU images" or "make each SKU into a listing image" must go through Step 2.5 before deciding native vs AI.

**Mixed requests**:
- Content-changing AI operations usually run first.
- Final delivery operations such as resize, crop, compress, and format conversion usually run last.
- Only run crop/resize first when the user explicitly requires a fixed canvas before editing.

> If the Agent toolset lacks a dedicated resize/compress tool, inform the user that this operation is not supported by the AI image tools and suggest alternatives.

### Step 2.5 — SKU Asset Workflow

SKU requests are not always native-only. First classify the user's SKU intent before selecting tools.

| SKU Intent | User Signals | Route |
|------------|--------------|-------|
| **Extract existing SKUs** | "split/crop/separate each SKU", "do not change products", "export each visible style" | Use native crop/segmentation/background removal first. Do not redraw products. |
| **Standardize SKU listing images** | "make each SKU into a listing/main image", "white background SKU images", "Alibaba SKU images", "same style/composition for each SKU" | First isolate each visible SKU, then use `image_edit` per SKU with strict product fidelity. Final resize/format is native. |
| **Generate SKU variants** | "generate colors/styles", "create red/blue/green variants", "make more SKU options" | Use `image_edit` with SKU Color Change when a reference exists; use generation only when the user explicitly asks for new variants. |

Rules:
- Never invent SKU count, colors, materials, or variants unless the user explicitly requested them.
- For batch SKU work, first identify the expected output count. If the count is unclear or visual separation is ambiguous, ask for confirmation.
- For listing-ready SKU images, output one image per SKU. Do not satisfy a multi-SKU request with one combined image.
- Preserve each SKU's exact color, pattern, shape, material, labels, accessories, and visible details.
- Use AI only for listing standardization or requested variant generation; use native tools for pure extraction/crop/format delivery.

### Step 3 — Ambiguity Check

Evaluate whether the request contains enough information to proceed:

| Ambiguity Signal | Action |
|------------------|--------|
| No actionable verb ("edit this", "process these") | Ask what specific changes are needed |
| Safe default subjective requests ("make it cleaner / more professional / optimize") | Proceed with conservative visual cleanup; ask only if the desired outcome is unclear or risky |
| Context-only reply ("yes", "right", "go ahead") with no prior clear instruction | Ask what the user would like done |
| Folder/batch reference without per-image instructions | List files and ask what operation to apply |

| Ambiguity Type | Examples | Action |
|----------------|----------|--------|
| Blocking ambiguity | "edit this", "process these", folder with no operation | Ask user |
| Safe default ambiguity | "make it more professional", "optimize product image", "make it cleaner" | Proceed with safe visual defaults |

Safe visual defaults include cleaner background, balanced composition, soft natural lighting, sharper product presentation, corrected product centering, and preservation of product identity.

Do not add new claims, text, logos, certifications, dimensions, materials, or product features unless the user provides them.

Ask the user with specific, selectable options when the host provides a prompt UI; otherwise ask a concise plain-language question (e.g., "What would you like to do: change background, remove watermark, adjust colors, add text, or something else?").

### Step 4 — Multi-Intent Execution Planner

If the request contains **2 or more intents** (including mixed AI + non-AI), plan by output image and minimize AI calls. Decomposition is for reasoning; it does not automatically mean sequential execution.

1. **Identify** all requested intents and the expected output count.
2. **Separate native delivery intents**: resize, crop, compress, rotate, and format conversion should usually run last with native tools and should not trigger an AI call.
3. **Group AI intents by output image**: if several visual changes belong to the same final image, merge them into one prompt when the tool can satisfy them together.
4. **Load references for every matched scene** using the Reference Loading Contract.
5. **Choose execution mode**:
   - `single_purpose`: only when the request exactly matches one dedicated task and no other visual/layout/platform changes are needed.
   - `merged_simple`: one `simple_generation` call for compatible product-fidelity edits such as scene/background, white/light hero styling, centering, shadow, lighting cleanup, local cleanup, logo placement, or product color change.
   - `merged_complex`: one `complex_generation` call for dense layouts, selling-point images, comparison grids, tech packs, or multi-region visual design in a single output.
   - `true_sequential`: only when a previous output is required before the next step, when tool limitations force it, or when the user explicitly requests separate intermediate outputs.
6. **Execute the minimum number of AI calls needed** for the requested output count, then apply native delivery operations last.
7. **Aggregate** results and state any skipped or native-only operations.

**Cost guard**:
- Prefer one AI call per requested output image.
- Do not multiply calls by the number of detected intents when the intents can be expressed in one prompt.
- If a plan would require more AI calls than the requested output count, compress the plan first; ask or explain only when compression would reduce quality or violate safety/tool constraints.
- Platform image sets and SKU batches may require multiple calls because the user expects multiple output images, but each output should still use the fewest feasible calls.

**Merge examples**:

| Request | Preferred Execution |
|---------|---------------------|
| "Make an Amazon main image with white background, centered product, natural shadow" | Load Platform + White Background, then one `simple_generation` call |
| "Remove small clutter, change to white background, and improve lighting" | Load relevant references, then one `simple_generation` call unless clutter is a complex authorized watermark |
| "Change product to red and put it on a gray studio background" | Load SKU Color Change + Scene Image, then one `simple_generation` call |
| "Add my logo and make it a clean listing hero" | Load Logo Customization + Platform/White Background if relevant, then one `simple_generation` call |
| "Create 5 Alibaba listing images" | One planned call per requested output image, not one call per sub-intent inside each image |

Use `true_sequential` for cases such as isolating each SKU before standardization, removing a dense watermark before a high-fidelity edit, or generating separate tech-pack drawings requested as distinct outputs.

### Step 5 — Scene Routing

Match the request against the Scene Router below (Priority 1 → 4). Use the first matching priority level.

---

## Scene Router

### Priority 1 — Platform Product Image (Composite)

| Trigger | Reference | Action |
|---------|-----------|--------|
| User mentions a specific e-commerce platform (Amazon, eBay, Walmart, Shopify, Etsy, AliExpress, TikTok Shop, Shopee, Lazada, Alibaba.com, 1688) AND requests main image / image set / listing images | `references/platform-product-guidelines.md` | Must load platform specs, then load each selected output scene reference. Plan by requested output image and merge compatible edits per Step 4. |

Platform Product Image is a composite workflow — it consults platform requirements first, then delegates to White Background, Scene Image, Model Showcase, etc. as sub-tasks.

**Sub-task execution rules:**
- When the user uploaded product images, ALL sub-tasks MUST use `image_edit`. Never use `image_generate` when reference images exist.
- Only **Selling Point Image** and **Logo Design** sub-tasks may trigger user clarification (for selling-point confirmation or brand context). All other sub-tasks execute directly unless safety or missing required inputs block execution.

**Platform image set planner**:
When the user requests multiple listing images (e.g. "3/5/6/11 main images", "main images + detail page images", "Alibaba.com product image set"), create an execution plan before generation:

1. Hero/main image — full product, clean white or light background, no promotional text unless the platform allows it
2. Scene image — B2B or use-context background while preserving the product
3. Detail image — visible material/structure close-up only
4. Selling-point image — only user-provided or visible/verifiable claims
5. Scale/usage image — only if supported by the image or user request
6. Packaging/accessory image — only if visible or user-provided

Rules:
- Generate or edit one final image per planned output. Do not split a single planned output into multiple AI calls unless Step 4 requires `true_sequential`.
- If the tool can only produce one image per call, explicitly run multiple calls or state the limitation.
- Output count must match the requested count when feasible; otherwise explain which planned images were produced and which remain.
- For uploaded product images, every planned image must preserve product identity and use `image_edit`.

### Priority 2 — Single-Purpose Scenes

These use dedicated `task_type` values that perform only one function. They are valid only for exact single-operation requests:

| Scene | Trigger Keywords | Reference | task_type |
|-------|-----------------|-----------|-----------|
| **White Background** | white background, pure white bg, remove background to white | `references/white-background.md` | `white_background` |
| **Watermark / Element Removal** | remove authorized watermark, remove URL/contact/QR overlay, remove accidental overlay, remove non-product object/clutter | `references/remove-watermark.md` | `watermark_removal` |
| **HD Upscale** | upscale, enhance resolution, make clearer, sharpen, higher quality | `references/hd-upscale.md` | `hd_upscale` |

**Single-Purpose Use Rule**:
Use these task_types only when the user's request exactly matches the single operation and does not require layout, composition, lighting, platform compliance, text editing, ratio change, or multiple visual changes.

Watermark removal is only allowed when the user owns the image or has rights to edit it. Do not help remove third-party copyright marks, platform watermarks, photographer signatures, or ownership identifiers to bypass licensing. Allowed cases include removing the user's own watermark, accidental overlays, stains, dust, scanner marks, or non-ownership visual clutter.

Do not treat every "delete text/logo" request as Watermark Removal. If the target is product/package text, a product brand mark, or user-specified local text, route to Text Editing's local text removal flow. If the target looks like an ownership or licensing mark and rights are unclear, ask for confirmation before editing.

**Single-Purpose Fallback**:
Switch to a merged `simple_generation`, merged `complex_generation`, or `true_sequential` plan when:
- The request contains 2 or more intents
- The user asks for platform-ready or listing-ready output
- The user uses broad outcome language such as "professional", "optimized", "cleaner", "main image", or "selling image"
- The user specifies a non-1:1 aspect ratio
- The user requests follow-up edits after the initial single-purpose operation

### Priority 3 — Specialized Editing Scenes

| Scene | Trigger Keywords | Reference | task_type |
|-------|-----------------|-----------|-----------|
| **Scene Image** | scene shot, change/swap background, place in environment, lifestyle shot | `references/scene-image.md` | `simple_generation` (preferred when product preserved) |
| **SKU Color Change** | recolor product, change product color, SKU color variant | `references/sku-color-change.md` | `simple_generation` / `complex_generation` |
| **Logo Customization** | print logo on product, logo mockup, emboss/engrave/stamp logo | `references/logo-customization.md` | `simple_generation` |
| **Model Showcase** | model photo, add model, model wearing/holding product | `references/model-showcase.md` | `simple_generation` |
| **Image Detail** | detail shot, zoom in, close-up of texture/stitching | `references/image-detail.md` | `simple_generation` |
| **Selling Point Image** | selling point image, highlight features, comparison image, vs competitors | `references/selling-point.md` | `simple_generation` / `complex_generation` |
| **Image Translation** | translate text in image, convert image text to [language] | `references/image-translation.md` | `simple_generation` |
| **Text Editing** | change text in image, replace text, fix typo, update price/date | `references/text-editing.md` | `simple_generation` / `complex_generation` |
| **Logo Design** | design a logo, create brand mark, logo from scratch | `references/logo-design.md` | `complex` for generation / `simple_generation` or `complex_generation` for editing |
| **Tech Pack** | tech pack, dimension drawing, manufacturing spec, assembly diagram | `references/tech-pack.md` | `complex_generation` |

> **Image Translation mandatory rule**: When the user requests an edited translated image, load `references/image-translation.md` and call `image_edit` after required inputs are available. Do not substitute a text-only translation for an image-edit request.

### Priority 4 — General (Fallback)

If no specialized scene matches, use semantic instructions with `simple_generation` or `complex_generation` based on complexity. Refer to `references/style-guide.md` for prompt enrichment vocabulary (atmosphere, composition, lighting, materials).

### Key Disambiguation Rules

These cover the most commonly confused routing decisions:

| Ambiguous Request | Correct Route | Why |
|-------------------|---------------|-----|
| "Change background to white" | **White Background** | Pure white (#FFFFFF) → single-purpose task |
| "Change background to kitchen / blue / gray" | **Scene Image** | Any non-pure-white background = scene swap |
| "Recolor the product body" | **SKU Color Change** | Product color, not background |
| "[Platform name] + white background main image" | **Platform** → White Background | Platform keyword → Priority 1 first |
| "Zoom in on zipper detail" vs "Highlight waterproof feature" | **Image Detail** vs **Selling Point** | Pure zoom (no text) → Detail; zoom + marketing copy → Selling Point |
| "Lifestyle selling point image" / "Detail with callouts" | **Selling Point Image** | Marketing expressions + any other scene keyword → Selling Point wins |
| "Make image clearer" vs "Generate a 2K image" | **HD Upscale** vs Resolution Routing | No resolution specified → upscale; explicit resolution → see below |
| "Design a logo" vs "Print logo on product" | **Logo Design** vs **Logo Customization** | From scratch → Design; apply existing → Customization |
| "Translate text in image" vs "Change price from 50% to 70%" | **Image Translation** vs **Text Editing** | Cross-language → Translation; same-language replacement → Text Editing |
| "Delete specified product text" vs "Remove authorized watermark/overlay" vs "Add marketing copy" | **Text Editing** vs **Watermark Removal** vs **Selling Point** | Product/package text removal → Text Editing local removal; authorized watermark/contact/QR/non-product overlay removal → `watermark_removal`; add new text + layout → Selling Point |
| "Tech pack / dimension drawing" vs "Mark dimensions as selling point" | **Tech Pack** vs **Selling Point ③** | Production/OEM specs → Tech Pack; marketing display → Selling Point |

### Strict Product Fidelity Mode

Enable this mode whenever the user asks to keep the product unchanged, produce platform/listing images from a reference, remove/replace text while preserving the product, make a white-background hero, or change only the surrounding scene/background.

Append this constraint to all relevant `image_edit` prompts:

```
Keep the product exactly unchanged — preserve geometry, color, texture, labels, and camera angle.
Only change: [describe allowed changes here].
Do not redraw, simplify, or invent any product detail.
```

Keep the constraint concise (≤3 lines). Verbose constraint lists (enumerating 20+ protected items) do not improve model compliance and can reduce prompt execution quality.

When product fidelity conflicts with a more creative instruction, product fidelity wins unless the user explicitly asks to redesign the product.

**Task type rule**: When Strict Product Fidelity Mode is active, prefer `simple_generation` over `complex_generation` unless the loaded reference requires dense layout or annotations. In many runtimes, complex edit modes are more likely to affect the whole image, increasing product drift risk.

**Selling Point Image priority rule**: When a request combines marketing expressions (selling point, copy, layout, callout, comparison) with other scene keywords (detail, scene, model), route to **Selling Point Image**. Only Selling Point Image can output copy + layout + visual anchors together.

### Resolution Routing

When the user specifies an output resolution:

| Request | Action |
|---------|--------|
| "Make it clearer / sharpen" (no resolution specified) | Use `hd_upscale` |
| "Generate at 1K / 2K" or explicit resolution | Use `simple_generation` with `resolution` parameter (if tool supports it), otherwise `hd_upscale` |
| "4K" or higher | Prefer native high-resolution generation if supported. If unsupported, generate at the highest available resolution, then upscale. |

### Task Type Safety Rules

`task_type` is an execution hint, not the user's intent.

Before selecting a task_type:
1. Identify the user's desired final outcome.
2. List all required visual changes.
3. Check whether a single-purpose task_type can satisfy all required changes.
4. If not, use a merged `simple_generation`, merged `complex_generation`, or `true_sequential` plan only when required by Step 4.

Use single-purpose task_types only when the user requests exactly one operation:
- `white_background`: only pure white background replacement
- `hd_upscale`: only clarity/resolution improvement
- `watermark_removal`: authorized removal of watermarks, URLs, contact info, QR codes, accidental overlays, stains, dust, scanner marks, or non-product visual clutter. Product/package text and product brand marks are not this route.

Do not use single-purpose task_types for:
- Platform-ready product images
- General image optimization
- "Make it professional"
- Mixed requests
- Follow-up refinements
- Layout, text, selling-point, or composition changes
- Requests involving product coverage, shadows, centering, lighting, or platform compliance

### Task Type Misrouting Guard

| User Request | Avoid | Prefer |
|-------------|-------|--------|
| "Make this an Amazon main image" | `white_background` only | Platform workflow + prompted edit |
| "Make it cleaner/professional" | `hd_upscale` only | Product cleanup with safe defaults |
| "Remove text and make white background" | `watermark_removal` only | Load Text Editing or Watermark Removal + White Background; prefer one merged `simple_generation` unless true sequential is required |
| "Optimize this product photo" | Single-purpose task_type | Product cleanup / platform intent |
| "Change background and improve lighting" | `white_background` | Load Scene Image; use one merged `simple_generation` |
| "Delete logo from product" | `watermark_removal` blindly | Clarify ownership/intent if needed |
| "Turn this into a listing image" | Any single-purpose task_type | Platform or product image workflow |

### Simple vs Complex task_type

| Criteria | `simple` / `simple_generation` | `complex` / `complex_generation` |
|----------|-------------------------------|----------------------------------|
| Edit scope | Single region, localized | Multi-region or full-image overhaul |
| Product preserved? | Yes — this is the safe choice | Higher redraw risk |
| Elements modified | ≤2 | ≥3 or major composition change |
| Typical use | Background swap, scene change, single recolor, logo stamp, product-on-white | Poster with selling points, comparison grid, infographic, tech pack |

**When in doubt, use `simple_generation`**. The downside of `simple_generation` on a complex task is lower layout quality; the downside of `complex_generation` on a fidelity task is product destruction.

### `complex_generation` Risk Guard

`complex_generation` is higher-risk for product-fidelity tasks because many image-edit runtimes treat complex edits as broader redraws rather than localized edits. Use it only when the requested output genuinely needs dense layout, annotations, comparison grids, or full-image design composition.

**Default to `simple_generation`** unless the task genuinely requires complex layout:

| Scenario | Correct task_type |
|----------|------------------|
| Background swap / scene change (product preserved) | `simple_generation` |
| Single-region edit (recolor, remove object, add logo) | `simple_generation` |
| White/light hero image from product photo | `simple_generation` |
| Platform main image (product preserved) | `simple_generation` |
| Model showcase with product | `simple_generation` |
| Localized product/package text removal | `simple_generation` via Text Editing local removal |
| Authorized watermark/contact/QR/non-product overlay removal | `watermark_removal` |
| Dense annotations / selling-point layout / comparison grid | `complex_generation` |
| Multi-region independent edits in one image | `complex_generation` |
| Full creative poster / heavy compositional redesign | `complex_generation` |
| Tech pack with dimension callouts | `complex_generation` |

**Rule of thumb**: If the product must stay unchanged, use `simple_generation`. The "complex" in the user's request description does not mean you should use `complex_generation` — a visually rich background or detailed scene is still a `simple_generation` task when the product is preserved.

If using `complex_generation` with a product reference, always enable Strict Product Fidelity Mode.

---

## Prompt Construction

### Generation Prompt Formula

```
[Shot type] of [Subject] in [Setting], [Action/State].
[Style], [Composition], [Lighting], [Color palette], [Quality].
```

| Element | Description | Examples |
|---------|-------------|----------|
| Subject | What to depict (be specific) | "ginger tabby cat", "ergonomic wireless headphones" |
| Setting | Environment/location | "windowsill with afternoon sunlight", "minimalist studio" |
| Style | Overall aesthetic | "cinematic", "watercolor", "flat vector" |
| Composition | Camera/framing | "close-up", "wide-angle", "rule-of-thirds" |
| Lighting | Light source and mood | "golden hour", "soft diffused", "Rembrandt lighting" |
| Color | Palette direction | "Morandi palette", "high saturation", "monochromatic" |
| Quality | Detail level | "8K", "hyperrealistic", "sharp detail" |

For text in images, use explicit quotes: `Display "LIMITED EDITION" in bold serif font`.

### Editing Prompt Formula

```
[Edit instruction targeting specific area].
[Preservation clause (concise, ≤3 lines)].
```

**Preservation clause template** (append to every edit prompt):

```
Keep the product exactly unchanged — preserve geometry, color, texture, labels, and camera angle.
Only change: [specific allowed changes].
Do not redraw, simplify, or invent any product detail.
```

Keep it concise. Long enumeration lists (20+ protected items) do not improve compliance and may reduce model execution quality. The model responds better to clear, short constraints than to exhaustive lists.

**Example — Scene change**:
```
Place the product on a modern kitchen countertop with warm morning light.
Keep the product exactly unchanged — preserve geometry, color, texture, labels, and camera angle.
Only change: background/scene.
Do not redraw, simplify, or invent any product detail.
```

---

## Result Check

After receiving a generation or editing result:

1. **Preservation audit**: Compare the result against the preservation clause. If the model altered protected elements (product shape distorted, text removed, colors shifted), retry with a stronger constraint — e.g., add "CRITICAL:" prefix, list each protected element individually, or reduce edit scope.
2. **Intent completeness**: Verify all user-requested changes are present. If a sub-task from Step 4 was missed, execute the remaining sub-tasks on the current output.
3. **Quality gate**: If the result is clearly unusable (heavy artifacts, wrong subject, garbled text), inform the user and offer to retry with adjusted parameters (e.g., switch `simple_generation` → `complex_generation`, or simplify the prompt).

Hard failure conditions:
- Product shape, structure, SKU color/pattern, packaging text, logo, handle, seam, hole, accessory, or camera angle changed when not requested
- A crop/split/resize/format task was handled by generating a new product image
- Multi-image or multi-SKU output count does not match the requested/confirmed count
- White-background output changes the product or leaves damaged/blurred edges
- Text editing/removal causes garbled text, misspellings, or modifies unspecified text
- Platform hero image includes prohibited overlays, watermarks, contact information, or unsupported claims
- User requested "do not change the product" but the result redraws or reimagines the product

### Scene Acceptance Criteria

| Scene | Acceptance Criteria |
|-------|---------------------|
| White Background | Background is pure white or near #FFFFFF; product shape unchanged; edges clean |
| HD Upscale | More detail without changing identity, color, text, or layout |
| Watermark / Element Removal | Removed target element only; no damage to product or surrounding content |
| Text Editing | Exact requested text; readable; no garbled characters |
| Product Cleanup | Product identity preserved; lighting/background improved; no invented claims |
| Selling Point Image | No fabricated claims; labels readable; text does not cover product |
| Platform Hero | Meets platform background, text, watermark, ratio, and product coverage rules |
| Logo Design | Original, legible, commercially safe, not similar to known trademarks |

> Do NOT silently retry indefinitely. After 2 failed attempts at the same task, inform the user of the limitation and suggest alternatives.

---

## Tool Contract / Host Mapping

Concrete tool names may vary by runtime. Map workflow intent to available tools.

Required conceptual operations:
- Text-to-image generation
- Image-to-image editing
- Native resize/crop/compress/format conversion, if available
- User clarification / selection prompt, if available

For image generation:
- Required: prompt
- Optional: aspect_ratio, resolution, task_type

For image editing:
- Required: reference_images, prompt or task_type
- Optional: aspect_ratio, resolution

If the runtime lacks a native resize/compress/format tool, use available local image-processing libraries when permitted. If unavailable, explain the limitation to the user.

## Tool Reference

### Canonical task_type values

For `image_generate`:
- `simple`
- `complex`

For `image_edit`:
- `white_background`
- `hd_upscale`
- `watermark_removal`
- `simple_generation`
- `complex_generation`

### image_generate

For generating images from scratch (no reference image).

| task_type | When to Use |
|-----------|-------------|
| `simple` | Single subject, simple scene, basic composition |
| `complex` | Multi-element, detailed poster, 3D render, multi-image set |

### image_edit

For editing an existing image.

| task_type | When to Use |
|-----------|-------------|
| `white_background` | Pure white background replacement (single-purpose) |
| `hd_upscale` | Resolution/sharpness enhancement (single-purpose, no prompt needed) |
| `watermark_removal` | Remove authorized watermark/contact/QR overlays or non-product visual clutter (single-purpose). Do not use for product/package text or unclear ownership marks. |
| `simple_generation` | Straightforward edits, background swap, scene change, single-region changes. **Preferred when product must stay unchanged.** |
| `complex_generation` | Multi-region layout, poster, infographic, collage. **Do NOT use for product-fidelity edits** — those should use `simple_generation`. |

---

## Aspect Ratio

### Supported Values

```
1:1 | 2:3 | 3:2 | 3:4 | 4:3 | 4:5 | 5:4 | 9:16 | 16:9 | 21:9
```

### Selection Rules

1. **User specified a supported ratio** → use it directly
2. **User specified an unsupported ratio** (e.g., 5:3) → inform user and ask to choose from supported list
3. **Single-purpose scenes** (white_background, hd_upscale, watermark_removal) **only support 1:1**. If the user needs a different ratio, auto-switch to `simple_generation`
4. **User did not specify** →
   - Single-purpose scenes → default `1:1`
   - Other scenes with uploaded image → match closest ratio from the table below
   - Other scenes without image → default `1:1`

### Auto-Match Table (for uploaded images without user-specified ratio)

| Image Shape | W:H Range | Best Match |
|-------------|-----------|------------|
| Square | 0.9 – 1.1 | `1:1` |
| Slightly tall | 0.75 – 0.9 | `4:5` |
| Portrait | 0.6 – 0.75 | `3:4` |
| Tall portrait | 0.5 – 0.6 | `2:3` |
| Very tall | < 0.5 | `9:16` |
| Slightly wide | 1.1 – 1.35 | `5:4` |
| Landscape | 1.35 – 1.6 | `4:3` |
| Wide landscape | 1.6 – 1.8 | `3:2` |
| Widescreen | 1.8 – 2.2 | `16:9` |
| Ultra-wide | > 2.2 | `21:9` |

> Compute W/H ratio of the uploaded image and find the matching range. If the closest ratio deviates >10% from the original, briefly inform the user about potential cropping.

---

## Multilingual Handling

When the user's input is not in English:

1. **Detect the input language**
2. **Preserve key terms**: Embed the user's original nouns/descriptions directly into the prompt rather than translating them (translation can distort meaning)
3. **Build prompts in English**: The image model works best with English prompts, but anchor key concepts from the original language
4. **Respond in the user's language**

> Example: User writes "A máquina parada (dor financeira)" (Portuguese)
> → Extract: "máquina parada" = stopped machine, "dor financeira" = financial pain
> → Prompt uses: "idle/stopped CNC machine, conveying financial loss and downtime frustration"
> → NOT: "professional, precise, clean machine" (semantic reversal)

---

## Batch Operations

When the user references a folder or multiple images:

1. List the images in the folder/selection
2. If the user has not specified what to do per image, ask for the operation before editing
3. If all images need the same operation → batch-execute the same scene
4. If different images need different operations → classify and route individually
5. **Never guess-edit** folder contents without explicit instructions
