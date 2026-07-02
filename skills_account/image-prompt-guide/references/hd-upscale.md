# HD Upscale

## Routing Header

- **Load when**: user asks to upscale, sharpen, enhance clarity, restore resolution, or make an existing image clearer without content changes.
- **Do not load when**: user asks only to increase file size, convert format, resize dimensions, crop, or change visual content.
- **Merge notes**: do not treat upscale as a separate paid AI step when the user mainly wants native delivery sizing. If content edits are needed, perform content edits first and upscale only when quality is still insufficient or the user explicitly requested it.
- **Hard stop**: this scene must not remove watermarks, change backgrounds, fix layout, edit text, or alter any image content.

## Scene Description

Enhance the resolution and sharpness of an existing image without modifying its content, composition, colors, or elements.

> **Hard constraint**: This scene only enhances clarity. It does not remove watermarks, change backgrounds, adjust elements, or alter image content in any way.

## Apply Method: Tool-Only (no prompt needed)

Pass the image directly to the tool. No prompt construction required.

## Tool Invocation

- Tool: `image_edit`
- task_type: `hd_upscale`
- prompt: **not needed**

## Content-Type Pre-Check

Before calling `hd_upscale`, the Agent should assess the image content type:

| Content Type | Recommendation |
|-------------|----------------|
| Product photos, natural scenes, portraits | Proceed normally with `hd_upscale` |
| **Text-heavy images** (posters, UI screenshots, infographics, documents) | **Warn the user**: "HD upscale may cause text distortion or garbled characters on text-heavy images. Consider obtaining a higher-resolution source file or using a non-AI upscaling tool instead." |
| **File size requests** ("I need it to be 2MB", "output is too small") | **This is NOT an AI task**. Route to resize tool or quality-parameter adjustment. Increasing file size ≠ increasing visual clarity. |

## Resolution Routing

When the user specifies an explicit output resolution (1K/2K/4K) rather than "make it clearer":

```
IF image_edit tool has a `resolution` parameter:
    → Use simple_generation with the resolution parameter
ELSE:
    → Use hd_upscale

For 4K or higher requests: prefer native high-resolution generation if supported. If unsupported, generate at the highest available resolution, then upscale.
```

| User Request | image_edit has `resolution` param | image_edit lacks `resolution` param |
|-------------|----------------------------------|-------------------------------------|
| "Generate 1K/2K image" | `simple_generation` (pass resolution) | `hd_upscale` |
| "Generate 4K image" | Native high-resolution generation if supported; otherwise highest supported resolution + `hd_upscale` | `simple_generation` then `hd_upscale` |
| "Make it clearer / sharpen" | `hd_upscale` | `hd_upscale` |

**Key distinction**:
- "Make clearer / sharpen / upscale" = enhance existing image → always `hd_upscale`
- "Generate at XK resolution" = specified output resolution → check tool capabilities first

## Notes

- **1:1 aspect ratio only**: if the user requests a non-1:1 ratio, auto-switch to `simple_generation` (see SKILL.md aspect ratio rules)
- **Single-purpose constraint**: if the request includes 2 or more intents, platform/listing readiness, composition changes, lighting changes, or broad optimization language, use a merged `simple_generation`, merged `complex_generation`, or `true_sequential` plan only when required by SKILL.md Step 4.
- **No content modification**: this scene must not change composition, colors, elements, or background — only resolution and sharpness
- **4K support depends on the runtime**: use native high-resolution generation when available; otherwise use highest supported generation followed by upscale.
