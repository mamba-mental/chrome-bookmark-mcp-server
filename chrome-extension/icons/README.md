# Chrome Extension Icons

This folder contains the icon assets for the MCP Chrome Bookmark Manager extension.

## Icon Sizes

- `icon16.png` - 16x16px (for browser UI)
- `icon32.png` - 32x32px (for browser UI @2x)
- `icon48.png` - 48x48px (for extensions page)
- `icon128.png` - 128x128px (for Chrome Web Store)

## Icon Design

The icons feature a bookmark symbol with AI/robot elements to represent the intelligent bookmark management capabilities.

## Generating Icons

### From SVG Sources

The `.svg` files are the source vectors. To generate PNG versions:

1. Open `convert-to-png.html` in a browser
2. The page will automatically convert SVGs to PNGs
3. Right-click and save each generated PNG

### Using Python Script

Alternatively, run the Python script to generate placeholder icons:

```bash
python generate-placeholders.py
```

This will create basic placeholder icons if the actual icons are missing.

## Icon Requirements

- Must be PNG format
- Must be exact dimensions (16x16, 32x32, 48x48, 128x128)
- Should have transparent background
- Should be optimized for file size
- Should follow Chrome's design guidelines

## Color Scheme

- Primary: #2563eb (Blue)
- Secondary: #1e293b (Dark)
- Accent: #10b981 (Green for AI indicator)
