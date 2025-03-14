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
    
    # Get all PNG files
    image_files = glob.glob("image-data/pixel_art_*8x8*.png")
    if not image_files:
        print("No 8x8 image files found in 'image-data' directory")
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
