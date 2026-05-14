#!/usr/bin/env python3
"""
Create dragon shield icon from scratch
"""
from PIL import Image, ImageDraw
import os

def create_dragon_icon():
    """Create a simple dragon shield icon"""
    
    # Create image
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Shield background - dark metal
    shield_color = (80, 80, 100, 255)
    border_color = (200, 200, 220, 255)
    
    # Draw shield outline (shield shape)
    points = [
        (128, 20),      # top center
        (210, 60),      # top right
        (230, 140),     # middle right
        (210, 200),     # bottom right
        (128, 230),     # bottom center
        (46, 200),      # bottom left
        (26, 140),      # middle left
        (46, 60),       # top left
    ]
    
    # Draw shield fill
    draw.polygon(points, fill=shield_color, outline=border_color)
    draw.polygon(points, outline=border_color, width=3)
    
    # Draw dragon eye (red glow)
    eye_x, eye_y = 128, 100
    draw.ellipse(
        [(eye_x - 15, eye_y - 15), (eye_x + 15, eye_y + 15)],
        fill=(255, 80, 0, 255),
        outline=(255, 200, 0, 255)
    )
    draw.ellipse(
        [(eye_x - 8, eye_y - 8), (eye_x + 8, eye_y + 8)],
        fill=(255, 150, 0, 255)
    )
    
    # Draw simple dragon horns
    horn_color = (200, 180, 160, 255)
    
    # Left horn
    horn_left = [(110, 70), (95, 40), (105, 55)]
    draw.polygon(horn_left, fill=horn_color, outline=border_color)
    
    # Right horn
    horn_right = [(146, 70), (161, 40), (151, 55)]
    draw.polygon(horn_right, fill=horn_color, outline=border_color)
    
    # Dragon snout/mouth area
    snout_color = (150, 140, 130, 255)
    draw.ellipse(
        [(110, 120), (146, 150)],
        fill=snout_color,
        outline=border_color
    )
    
    # Mouth line
    draw.line([(110, 135), (146, 135)], fill=(80, 70, 60, 255), width=2)
    
    # Scales pattern
    scale_color = (100, 100, 120, 200)
    for y in range(140, 200, 25):
        for x in range(80, 180, 25):
            draw.ellipse(
                [(x - 8, y - 8), (x + 8, y + 8)],
                fill=scale_color,
                outline=(120, 120, 140, 150)
            )
    
    return img

# Create icon
img = create_dragon_icon()

# Create assets folder if needed
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(assets_dir, exist_ok=True)

# Save as ICO with multiple sizes
icon_path = os.path.join(assets_dir, 'icon.ico')
img.save(
    icon_path,
    format='ICO',
    sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
)

print(f"✓ Dragon shield icon created!")
print(f"  Location: {icon_path}")
print(f"  Size: {os.path.getsize(icon_path) / 1024:.1f} KB")
print(f"\nReady to build EXE with icon!")
