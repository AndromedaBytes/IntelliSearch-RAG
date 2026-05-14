#!/usr/bin/env python3
"""
Convert PNG icon to ICO format for Windows EXE
"""
from PIL import Image
import os

# Source and destination paths
project_root = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(project_root, "app_icon.ico")

# The dragon shield icon image path (you'll need to save the image first)
# For now, create a placeholder 256x256 icon
# In production, replace with the actual dragon image

try:
    # Create a simple icon - this will be replaced with the actual dragon icon
    img = Image.new('RGB', (256, 256), color='black')
    
    # Convert to ICO format with multiple sizes
    img_copy = img.copy()
    img_copy.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    print(f"✓ Icon created at: {icon_path}")
    print(f"  Size: {os.path.getsize(icon_path)} bytes")
    
except Exception as e:
    print(f"✗ Icon creation failed: {e}")
    exit(1)
