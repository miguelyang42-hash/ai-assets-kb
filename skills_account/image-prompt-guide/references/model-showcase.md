# Model Showcase

## Routing Header

- **Load when**: user wants a model wearing, holding, or naturally demonstrating the product while preserving the original product photo background.
- **Do not load when**: user asks for model plus a new lifestyle/background scene or marketing copy only; load Scene Image or Selling Point as the primary scene.
- **Merge notes**: model constraints may be combined into Scene Image when the user wants both a model and a new environment. Use Selling Point when the model image also needs callouts or copy.
- **Hard stop**: do not change product identity, product proportions, or introduce unrelated scene elements in the pure Model Showcase flow.

## Scene Description

Generate a high-quality e-commerce model showcase image based on the product photo, with a model naturally demonstrating the product's wear or usage effect. Three variants based on user input.

> **Hard constraint**: This scene **preserves the original product image background**. It only adds a model to the scene.
> - If the user also wants to **change the background** (outdoor, street, home scene) → route to **Scene Image** and include model elements in the prompt
> - If the user wants **selling-point copy/layout/callouts** → route to **Selling Point Image** layout ④ (lifestyle)
> - Only use this scene when the user **just wants to add a model** without background change or marketing copy

## Apply Method: Direct Apply

Select the variant based on priority: A (has reference model photo) > B (specified model type) > C (neither).

## Prompt Templates

### Variant A — User uploaded a model reference photo

User provides both a product photo and a model photo:

```
Based on the uploaded product image and model image, generate a high-quality e-commerce model showcase photo:

## Requirements:
- Preserve the original product image background as closely as the tool allows.
- The product must remain fully consistent with the product image — do not change color, structure, proportions, texture, or details.
- The model should naturally showcase the product, making the product the visual focus and demonstrating wear or usage effect.
- The model's head must be retained in the generated image.
- Product and model proportions must be harmonious with no cognitive conflict.

## Arrange the showcase method based on product type:
- Apparel / Footwear / Sports & Outdoor gear: Model naturally wearing the item, showing overall fit and details.
- Accessories / Jewelry / Bags: Model wearing/carrying the item, highlighting product details.
- Home / Furniture / Appliances / Electronics / Beauty / Pet supplies / Personal care: Model naturally using or interacting with the product while maintaining the original background.
```

### Variant B — No model photo, but model type specified

User provides only a product photo and describes the desired model type (e.g., "Asian female model, mid-20s"):

```
Based on the uploaded product image, generate a high-quality e-commerce model showcase photo:

## Requirements:
- <model_type>
- Preserve the original product image background as closely as the tool allows.
- The product must remain fully consistent with the product image — do not change color, structure, proportions, texture, or details.
- The model should naturally showcase the product, making the product the visual focus and demonstrating wear or usage effect.
- The model's head must be retained in the generated image.
- Product and model proportions must be harmonious with no cognitive conflict.

## Arrange the showcase method based on product type:
- Apparel / Footwear / Sports & Outdoor gear: Model naturally wearing the item, showing overall fit and details.
- Accessories / Jewelry / Bags: Model wearing/carrying the item, highlighting product details.
- Home / Furniture / Appliances / Electronics / Beauty / Pet supplies / Personal care: Model naturally using or interacting with the product while maintaining the original background.
```

Replace `<model_type>` with the user's specified model description (e.g., "Asian female model, mid-20s", "European male model").

### Variant C — No model photo, no model type specified

User provides only a product photo without model preferences:

```
Based on the uploaded product image, generate a high-quality e-commerce model showcase photo:

## Requirements:
- Automatically select a model appearance appropriate for the product category (e.g., adult model for apparel, parent/infant for baby products). The model serves only as a display vehicle for the product — do not introduce new scene elements.
- Preserve the original product image background as closely as the tool allows.
- The product must remain fully consistent with the product image — do not change color, structure, proportions, texture, or details.
- The model should naturally showcase the product, making the product the visual focus and demonstrating wear or usage effect.
- The model's head must be retained in the generated image.
- Product and model proportions must be harmonious with no cognitive conflict.

## Arrange the showcase method based on product type:
- Apparel / Footwear / Sports & Outdoor gear: Model naturally wearing the item, showing overall fit and details.
- Accessories / Jewelry / Bags: Model wearing/carrying the item, highlighting product details.
- Home / Furniture / Appliances / Electronics / Beauty / Pet supplies / Personal care: Model naturally using or interacting with the product while maintaining the original background.
```

## Tool Invocation

- Tool: `image_edit`
- task_type: `simple_generation`

## Notes

- Variant selection priority: A (has model photo) > B (has model type description) > C (neither)
- Product color, structure, proportions, texture, and details must not be altered
- **Background preservation is a hard constraint**: preserve the original product image background as closely as the tool allows. Do not introduce new scene elements, outdoor environments, or re-create lighting atmosphere. For background changes, use Scene Image. For marketing copy, use Selling Point Image layout ④.
- Model's head must be retained
- Showcase method should match the product category (wearing, carrying, using, etc.)
