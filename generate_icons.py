#!/usr/bin/env python3
"""
Generate all icon files from logo.png
"""
from PIL import Image
import os

# Source logo file
logo_path = "public/logo.png"
output_dir = "public"

def resize_and_save(input_path, output_path, size, format=None):
    """Resize image and save to output path"""
    try:
        img = Image.open(input_path)
        
        # Convert RGBA to RGB only for JPEG (which doesn't support transparency)
        if format and format.upper() == 'JPEG' and img.mode == 'RGBA':
            # Create a white background for JPEG
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = background
        # Ensure RGBA mode for transparency support in PNG and ICO
        elif img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize maintaining aspect ratio, then crop to exact size
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Create a square canvas with transparent background (except for JPEG)
        bg_color = (255, 255, 255) if format and format.upper() == 'JPEG' else (0, 0, 0, 0)
        new_img = Image.new('RGB' if format and format.upper() == 'JPEG' else 'RGBA', (size, size), bg_color)
        
        # Paste resized image in center
        x_offset = (size - img.size[0]) // 2
        y_offset = (size - img.size[1]) // 2
        new_img.paste(img, (x_offset, y_offset), img if img.mode == 'RGBA' else None)
        
        # Save
        if format:
            new_img.save(output_path, format=format)
        else:
            new_img.save(output_path)
        
        print(f"Created {output_path} ({size}x{size})")
        return True
    except Exception as e:
        print(f"Error creating {output_path}: {e}")
        return False

def create_favicon(input_path, output_path):
    """Create favicon.ico with multiple sizes, preserving transparency"""
    try:
        img = Image.open(input_path)
        
        # Ensure RGBA mode for transparency support
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create favicon with multiple sizes (16x16, 32x32, 48x48)
        sizes = [(16, 16), (32, 32), (48, 48)]
        images = []
        
        for size in sizes:
            resized = img.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)
            # Use transparent background (RGBA with alpha=0)
            square = Image.new('RGBA', size, (0, 0, 0, 0))
            x = (size[0] - resized.size[0]) // 2
            y = (size[1] - resized.size[1]) // 2
            square.paste(resized, (x, y), resized if resized.mode == 'RGBA' else None)
            images.append(square)
        
        # Save as ICO with transparency support
        # Note: ICO format has limited transparency support, but we'll try to preserve it
        images[0].save(output_path, format='ICO', sizes=[(s[0], s[1]) for s in sizes])
        print(f"Created {output_path} (multi-size ICO with transparency)")
        return True
    except Exception as e:
        print(f"Error creating {output_path}: {e}")
        return False

def create_favicon_png(input_path, output_path, size=32):
    """Create PNG favicon with transparency support (better than ICO)"""
    try:
        img = Image.open(input_path)
        
        # Ensure RGBA mode for transparency support
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize maintaining aspect ratio
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Create square canvas with transparent background
        square = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        x = (size - img.size[0]) // 2
        y = (size - img.size[1]) // 2
        square.paste(img, (x, y), img)
        
        # Save as PNG (better transparency support than ICO)
        square.save(output_path, format='PNG')
        print(f"Created {output_path} ({size}x{size} PNG with transparency)")
        return True
    except Exception as e:
        print(f"Error creating {output_path}: {e}")
        return False

if __name__ == "__main__":
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found!")
        exit(1)
    
    # Generate all icon files
    print("Generating icon files from logo.png...")
    
    # Favicon - create both ICO (fallback) and PNG (better transparency)
    create_favicon(logo_path, os.path.join(output_dir, "favicon.ico"))
    create_favicon_png(logo_path, os.path.join(output_dir, "favicon.png"), 32)
    
    # Main icons
    resize_and_save(logo_path, os.path.join(output_dir, "icon.png"), 192)
    resize_and_save(logo_path, os.path.join(output_dir, "icon-192x192.png"), 192)
    resize_and_save(logo_path, os.path.join(output_dir, "icon-512x512.png"), 512)
    
    # Apple touch icons
    resize_and_save(logo_path, os.path.join(output_dir, "apple-touch-icon.png"), 180)
    resize_and_save(logo_path, os.path.join(output_dir, "apple-touch-icon-precomposed.png"), 180)
    
    # Create SVG (simple approach - reference PNG)
    # For a proper SVG, we'd need vector conversion, but we can create a simple SVG wrapper
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <image href="/icon-512x512.png" width="512" height="512"/>
</svg>'''
    
    with open(os.path.join(output_dir, "icon.svg"), 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Created {output_dir}/icon.svg")
    
    print("\nAll icon files generated successfully!")
