#!/usr/bin/env python3
"""
Convert dragon icon image to .ico format for IntelliSearch V2.exe
Usage: python setup_icon.py <path-to-image>
"""

import sys
from pathlib import Path
from PIL import Image

def convert_to_icon(image_path, output_path):
    """Convert image to multi-resolution ICO file"""
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create multiple sizes for better quality across different DPI settings
        sizes = [
            (256, 256),
            (128, 128),
            (64, 64),
            (48, 48),
            (32, 32),
            (16, 16)
        ]
        
        # Resize and save as ICO with all sizes
        img_resized = img.resize((256, 256), Image.Resampling.LANCZOS)
        img_resized.save(
            output_path,
            format='ICO',
            sizes=sizes
        )
        
        print(f"✓ Icon created successfully!")
        print(f"  Input:  {image_path}")
        print(f"  Output: {output_path}")
        print(f"  Size:   {output_path.stat().st_size / 1024:.1f} KB")
        print(f"  Sizes:  {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Conversion failed: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python setup_icon.py <path-to-dragon-icon-image>")
        print("\nSupported formats: PNG, JPG, GIF, BMP")
        print("Example: python setup_icon.py dragon_icon.png")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"✗ File not found: {input_path}")
        sys.exit(1)
    
    # Output to assets/icon.ico
    output_path = Path(__file__).parent / "assets" / "icon.ico"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if convert_to_icon(input_path, output_path):
        print("\n✓ Ready to build! Run: python build_exe.py")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
