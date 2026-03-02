# ComKit Color System

This directory contains the color configuration and styling system for the ComKit UI.

## 🎨 Color Palette

The application uses a beautiful modern color palette with the following shades:

- **50**: `#DAD7CD` - Lightest (backgrounds)
- **100**: `#A3B18A` - Light (subtle backgrounds)
- **200**: `#588157` - Medium Light (borders)
- **300**: `#3A5A40` - Medium (hover states)
- **400**: `#344E41` - Main (primary actions)
- **500**: `#2D3748` - Dark (pressed states)
- **600**: `#1A1E29` - Darker (text)
- **700**: `#0F172A` - Darkest (headings)

## 📁 Files

### `colors.css`
- Contains CSS custom properties and utility classes
- Imported globally in `app.vue` using CSS @import
- Provides CSS variables for easy access

### `../../config/colors.ts`
- TypeScript color configuration
- Helper functions for programmatic color access
- Easy to modify for theme changes

## 🛠️ Usage

### In Vue Components (Tailwind Classes)
```vue
<template>
  <!-- Background colors -->
  <div class="bg-primary-400">Main background</div>
  <div class="bg-primary-50">Light background</div>
  
  <!-- Text colors -->
  <p class="text-primary-600">Primary text</p>
  <p class="text-primary-400">Main text</p>
  
  <!-- Border colors -->
  <div class="border-primary-300">Primary border</div>
  
  <!-- Focus states -->
  <input class="focus:ring-primary-400 focus:border-primary-400" />
  
  <!-- Hover states -->
  <button class="bg-primary-400 hover:bg-primary-500">Button</button>
</template>
```

### In CSS/SCSS
```css
.my-component {
  background-color: var(--color-primary-400);
  color: var(--color-primary-600);
  border-color: var(--color-primary-300);
}
```

### Importing CSS in Vue Components
```vue
<style>
/* Use relative path for CSS files */
@import '../assets/styles/colors.css';

/* Your component styles */
.my-component {
  background-color: var(--color-primary-400);
}
</style>
```

### In TypeScript
```typescript
import { colors, getColor } from '~/config/colors'

// Access colors directly
const mainColor = colors.primary[400] // '#8E9B90'

// Use helper function
const textColor = getColor('primary', 600) // '#6B7A6D'
const bgColor = getColor('sage.50') // '#DCE2BD'
```

## 🎯 Customization

To change the entire theme:

1. **Modify the color values** in `../../config/colors.ts`
2. **Update CSS variables** in `colors.css`
3. **Update Tailwind config** in `tailwind.config.js`

### Example: Changing to Blue Theme
```typescript
// In config/colors.ts
export const colors = {
  primary: {
    50: '#EFF6FF',
    100: '#DBEAFE',
    200: '#BFDBFE',
    300: '#93C5FD',
    400: '#344E41', // Main blue
    500: '#3B82F6',
    600: '#2563EB',
    700: '#1D4ED8',
  },
  // ... rest of colors
}
```

## ⚠️ Important Notes

### CSS Import Method
- **Use CSS @import** in `<style>` blocks for CSS files
- **Do NOT use JavaScript imports** for CSS files in Vue components
- This prevents module resolution errors in Vitest/Nuxt

### Path Aliases
- `@/` and `~/` both point to the project root
- Use `../assets/...` for importing CSS in style blocks from app/ directory
- Use `@/assets/...` for importing CSS from other locations
- Use `~/config/...` for TypeScript imports

## 🧪 Testing

The color system is tested with the existing test suite. Run tests to ensure changes don't break functionality:

```bash
npm run test:run
```

## 🚀 Deployment

The color system is production-ready and will work automatically when the application is built and deployed.
