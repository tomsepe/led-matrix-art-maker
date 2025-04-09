"""
LED Matrix Pattern Converter

Converts 8x8 pixel art images into binary patterns for LED matrix displays.
Reads PNG files from the image-data directory and generates a Python module
with binary patterns that can be used by the LED matrix display scripts.

Features:
- Processes 8x8 PNG images from image-data directory
- Converts images to pure black and white (threshold at 127)
- Generates binary patterns (1 = LED on, 0 = LED off)
- Creates a Python module with all patterns in a dictionary
- Maintains original image names as pattern keys

Input:
- 8x8 PNG files in image-data directory
- Files must be named either 'pixel_art_*8x8*.png' or 'lowres_*.png'

Output:
- patterns/led_patterns.py containing a PATTERNS dictionary
- Each pattern is stored as a bytes object
- Binary format: 8 bytes, one per row, MSB first

Dependencies:
- Python 3.x
- Pillow (PIL) for image processing
"""

#!/usr/bin/env python3

from PIL import Image
import os
import glob
from datetime import datetime

def ensure_directories():
    """Create necessary directories if they don't exist"""
    for directory in ['patterns']:
        if not os.path.exists(directory):
            os.makedirs(directory)

def image_to_pattern(image_path):
    """Convert an 8x8 image to LED matrix pattern format"""
    try:
        # Open and verify image
        image = Image.open(image_path)
        
        # Verify image is 8x8
        if image.size != (8, 8):
            print(f"Skipping {image_path}: Invalid dimensions {image.size}, must be 8x8")
            return None
            
        # Convert to black and white
        image = image.convert('L')  # Convert to grayscale
        
        # Create pattern string
        pattern_lines = []
        
        # Add header
        pattern_name = os.path.basename(image_path).split('.')[0]
        # Remove 'lowres_' prefix if present
        if pattern_name.startswith('lowres_'):
            pattern_name = pattern_name[7:]
        pattern_lines.append(f"    '{pattern_name}': bytes([")
        pattern_lines.append("        # 8x8 matrix pattern")
        
        # Process each row
        for y in range(8):
            byte_val = 0
            # Process each pixel in the row
            for x in range(8):
                pixel = image.getpixel((x, y))
                # Convert pixel to bit (white = 1, black = 0)
                bit = 1 if pixel > 127 else 0
                byte_val |= (bit << (7 - x))
            
            # Format as binary literal
            binary_str = f"        0b{byte_val:08b},"
            pattern_lines.append(binary_str)
        
        # Close the pattern
        pattern_lines.append("    ]),")
        
        return "\n".join(pattern_lines)
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def convert_all_images():
    """Convert all 8x8 PNG images in image-data directory to pattern format"""
    ensure_directories()
    
    # Get all PNG files with either naming pattern
    image_files = (
        glob.glob("image-data/pixel_art_*8x8*.png") +
        glob.glob("image-data/lowres_*.png")
    )
    
    if not image_files:
        print("No 8x8 image files found in 'image-data' directory")
        print("Expected files matching either:")
        print("- image-data/pixel_art_*8x8*.png")
        print("- image-data/lowres_*.png")
        return
    
    print(f"Found {len(image_files)} images to convert")
    
    # Create patterns file
    with open("patterns/led_patterns.py", "w") as f:
        # Write file header
        f.write("# LED Matrix Patterns\n")
        f.write("# Auto-generated from 8x8 PNG files\n\n")
        f.write("PATTERNS = {\n")
        
        # Process each image
        for image_path in image_files:
            print(f"Converting {os.path.basename(image_path)}...")
            
            # Convert image to pattern
            pattern_text = image_to_pattern(image_path)
            if pattern_text is None:
                continue
                
            # Write pattern to file
            f.write(pattern_text)
            f.write("\n\n")
        
        # Close the patterns dictionary
        f.write("}\n")
    
    print(f"Patterns saved to patterns/led_patterns.py")

def main():
    print("Starting image conversion...")
    convert_all_images()
    print("Conversion complete!")

if __name__ == "__main__":
    main()
