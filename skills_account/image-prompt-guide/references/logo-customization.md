# Logo Customization

## Routing Header

- **Load when**: user has an existing logo or logo reference and wants it applied, printed, engraved, embossed, embroidered, stamped, or mocked up on a product.
- **Do not load when**: user asks to design a brand-new logo from scratch; load Logo Design instead.
- **Merge notes**: logo application can usually merge with listing-hero cleanup, white/light background, scene styling, and product-fidelity constraints in one `simple_generation` call.
- **Hard stop**: require both a product image and logo reference before compositing. Do not invent a logo.

## Scene Description

Composite the user's Logo image onto a product photo using a specified craft technique, placed at a contextually appropriate position for the craft type and product category.

## Apply Method: Concatenate

Select a craft technique (craft_prompt), then concatenate with the fixed compositing prompt.

## Prompt Template

### Step 1: Select Craft Technique (craft_prompt)

Choose one from the following list:

- Laser Engraving
- Screen Printing
- Heat Transfer
- Laser Printing
- Sticker / Transfer Decal
- Hot Stamping / Foil Stamping
- UV Printing
- Digital Printing
- Embroidery
- 3D Printing
- Embossing / Debossing
- Inkjet Printing
- Standard / Color Printing
- Single-color / Dual-color Printing

### Step 2: Build Complete Prompt

```
Composite the entire Logo from Image 2 onto the main product in Image 1, applying "{craft_prompt}" technique, and place it at a position appropriate for this craft type and the product category. Remove the background and edges around the Logo, retaining only the Logo itself for a clean, transparent blend. IMPORTANT: Keep the product in Image 1 unchanged — shape, color, texture, and details must remain consistent with the original.
```

Replace `{craft_prompt}` with the selected craft technique name.

### Example

If "Hot Stamping / Foil Stamping" is selected:

```
Composite the entire Logo from Image 2 onto the main product in Image 1, applying "Hot Stamping / Foil Stamping" technique, and place it at a position appropriate for this craft type and the product category. Remove the background and edges around the Logo, retaining only the Logo itself for a clean, transparent blend. IMPORTANT: Keep the product in Image 1 unchanged — shape, color, texture, and details must remain consistent with the original.
```

## Tool Invocation

- Tool: `image_edit`
- task_type: `simple_generation`
- Input: Two images — Image 1 (product photo) and Image 2 (Logo image)

## Notes

- Craft technique should be specified by the user or recommended based on product category
- Logo background and edges must be removed for clean integration
- Placement position must be appropriate for the selected craft and product type
- The product in Image 1 must remain completely unchanged
