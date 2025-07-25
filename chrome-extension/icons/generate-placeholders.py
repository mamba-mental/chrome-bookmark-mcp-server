#!/usr/bin/env python3
"""
Generate placeholder PNG icons for Chrome extension
Creates basic bookmark icons with AI indicator
"""

import os
from PIL import Image, ImageDraw

def create_bookmark_icon(size):
    """Create a simple bookmark icon with AI indicator"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate dimensions
    padding = size // 8
    bookmark_width = size - (padding * 2)
    bookmark_height = int(bookmark_width * 1.3)
    
    # Position bookmark
    x = padding
    y = (size - bookmark_height) // 2
    
    # Draw bookmark shape (blue)
    bookmark_color = (37, 99, 235, 255)  # #2563eb
    draw.rectangle(
        [(x, y), (x + bookmark_width, y + bookmark_height)],
        fill=bookmark_color
    )
    
    # Draw bookmark ribbon
    ribbon_width = bookmark_width // 3
    ribbon_points = [
        (x + bookmark_width // 2 - ribbon_width // 2, y + bookmark_height),
        (x + bookmark_width // 2, y + bookmark_height - ribbon_width // 2),
        (x + bookmark_width // 2 + ribbon_width // 2, y + bookmark_height),
    ]
    draw.polygon(ribbon_points, fill=bookmark_color)
    
    # Draw plus sign (white)
    plus_color = (255, 255, 255, 255)
    plus_thickness = max(1, size // 16)
    center_x = x + bookmark_width // 2
    center_y = y + bookmark_height // 2
    plus_size = bookmark_width // 3
    
    # Horizontal line
    draw.rectangle(
        [
            (center_x - plus_size // 2, center_y - plus_thickness // 2),
            (center_x + plus_size // 2, center_y + plus_thickness // 2)
        ],
        fill=plus_color
    )
    
    # Vertical line
    draw.rectangle(
        [
            (center_x - plus_thickness // 2, center_y - plus_size // 2),
            (center_x + plus_thickness // 2, center_y + plus_size // 2)
        ],
        fill=plus_color
    )
    
    # Draw AI indicator (green circle)
    if size >= 32:
        ai_color = (16, 185, 129, 255)  # #10b981
        ai_radius = size // 6
        ai_x = size - ai_radius - padding // 2
        ai_y = size - ai_radius - padding // 2
        
        draw.ellipse(
            [(ai_x - ai_radius, ai_y - ai_radius),
             (ai_x + ai_radius, ai_y + ai_radius)],
            fill=ai_color
        )
        
        # Draw small plus in AI indicator
        if size >= 48:
            ai_plus_size = ai_radius // 2
            ai_plus_thickness = max(1, ai_radius // 4)
            
            draw.rectangle(
                [
                    (ai_x - ai_plus_size // 2, ai_y - ai_plus_thickness // 2),
                    (ai_x + ai_plus_size // 2, ai_y + ai_plus_thickness // 2)
                ],
                fill=plus_color
            )
            
            draw.rectangle(
                [
                    (ai_x - ai_plus_thickness // 2, ai_y - ai_plus_size // 2),
                    (ai_x + ai_plus_thickness // 2, ai_y + ai_plus_size // 2)
                ],
                fill=plus_color
            )
    
    return img

def main():
    """Generate all required icon sizes"""
    sizes = [16, 32, 48, 128]
    
    print("Generating placeholder icons...")
    
    for size in sizes:
        icon = create_bookmark_icon(size)
        filename = f"icon{size}.png"
        icon.save(filename, "PNG", optimize=True)
        print(f"Created {filename} ({size}x{size})")
    
    print("\nPlaceholder icons generated successfully!")
    print("Note: These are basic placeholders. Consider creating custom icons for production.")

if __name__ == "__main__":
    # Check if PIL is installed
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Error: Pillow is not installed.")
        print("Install it with: pip install Pillow")
        exit(1)
    
    main()
