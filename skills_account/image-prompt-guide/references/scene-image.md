# Scene Image

## Routing Header

- **Load when**: user wants to change, replace, or generate the surrounding scene/background/environment while preserving the product.
- **Do not load when**: user wants only pure white background, only product recolor, only text editing, or only native resize/crop/format conversion.
- **Merge notes**: this is the preferred merge carrier for compatible edits such as background, lighting, mood, composition, cleanup, model-in-scene, and listing-style hero refinements when the product must stay unchanged.
- **Hard stop**: do not alter, redraw, recolor, simplify, or invent product details or hidden/occluded areas.

## Scene Description

Preserve the product subject while generating or replacing the surrounding scene/background to create a lifestyle or contextual visual.

> **Hard constraint**: Only the background/environment may change. The product itself must remain visually consistent with the original.
> - If occluded parts exist (covered by hands, packaging, objects, or the product itself), do NOT infer, reconstruct, or fabricate hidden content — only render what is actually visible in the original.

## Apply Method: Concatenate

Append the fixed constraint text after the user/Agent's scene description prompt.

## Task Type Selection

Use `simple_generation` by default when the user wants a new scene/background but the product must remain unchanged. A rich background alone is not enough reason to use `complex_generation`.

Use `complex_generation` only when the image also needs dense annotations, multi-region layout, selling-point design, comparison layout, or a full creative poster. If `complex_generation` is used with a product reference, apply Strict Product Fidelity Mode from `SKILL.md`.

## Prompt Template

### User/Agent Generated Part

Describe the desired scene. Example: "Place the product on a modern kitchen countertop with warm morning light"

### Fixed Constraint Text

```
Keep the main product in the image fully consistent with the original in shape, color, texture, material details, and structural features — do NOT alter, simplify, or reimagine any aspect of the product's appearance. For any parts that are occluded, blocked, or hidden in the original image (covered by hands, packaging, other objects, or the product itself), do NOT infer, reconstruct, or fabricate the hidden content — only render the visible portions actually shown in the original image. Only the surrounding scene/background may change as described.
Do not change product labels, logos, visible text, SKU color/pattern, handles, seams, holes, buttons, accessories, camera angle, or product proportions. Do not generate a new product photo.
```

### Complete Prompt Structure

```
{User/Agent scene description} + {Fixed Constraint Text above}
```

## Tool Invocation

- Tool: `image_edit`
- task_type: `simple_generation` or `complex_generation` (based on scene complexity)

## Notes

- **Product consistency is the core requirement**: shape, color, texture, material details, structural features, and all visible details must stay consistent with the original
- **No fabrication of occluded areas**: if the user wants to show angles hidden in the original (e.g., back, interior), inform them that area is not visible and suggest providing a clearer reference image
- **Only background/environment changes**: scene images only replace or reshape the environment, lighting, and atmosphere — never modify the product itself
- If the user asks for platform/listing images, route through the Platform Product Image planner first, then use this scene as one planned sub-task.
