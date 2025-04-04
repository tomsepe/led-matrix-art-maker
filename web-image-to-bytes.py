#!/usr/bin/env python3

from PIL import Image
import os
import glob
from datetime import datetime
import shutil

def ensure_directories():
    """Create necessary directories if they don't exist"""
    for directory in ['patterns', 'image-data']:
        if not os.path.exists(directory):
            os.makedirs(directory)

def process_web_image(image_path):
    """Process a 288x288 web image to 8x8 format and save to image-data"""
    try:
        # Open and verify image
        image = Image.open(image_path)
        
        # Verify image is 288x288
        if image.size != (288, 288):
            print(f"Skipping {image_path}: Invalid dimensions {image.size}, must be 288x288")
            return None
            
        # Get file modification time
        mod_time = os.path.getmtime(image_path)
        timestamp = datetime.fromtimestamp(mod_time).strftime("%Y%m%d_%H%M%S")
        
        # Create new filename
        new_filename = f"pixel_art_{timestamp}_8x8.png"
        new_path = os.path.join("image-data", new_filename)
        
        # Convert to grayscale first to remove color information
        image = image.convert('L')
        
        # Convert to pure black and white (binary) using a threshold
        # Any pixel > 127 becomes white (255), anything else becomes black (0)
        image = image.point(lambda x: 255 if x > 127 else 0, '1')
        
        # Now resize to 8x8 using nearest neighbor to maintain sharp edges
        small_image = image.resize((8, 8), Image.NEAREST)
        
        # Save the processed image
        small_image.save(new_path)
        print(f"Processed and saved: {new_path}")
        
        return new_path
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

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
        image = image.convert('L')
        
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
    """Convert all web drawings to 8x8 format and then to pattern format"""
    ensure_directories()
    
    # Process web drawings first
    web_images = glob.glob("led-matrix-web/web-drawings/*.png")
    if not web_images:
        print("No images found in 'led-matrix-web/web-drawings' directory")
        return
    
    print(f"Found {len(web_images)} web images to process")
    
    # Process each web image to 8x8 format
    processed_images = []
    for image_path in web_images:
        print(f"Processing {os.path.basename(image_path)}...")
        processed_path = process_web_image(image_path)
        if processed_path:
            processed_images.append(processed_path)
    
    if not processed_images:
        print("No images were successfully processed")
        return
    
    print(f"\nConverting {len(processed_images)} processed images to patterns...")
    
    # Create patterns file
    with open("patterns/led_patterns.py", "w") as f:
        # Write file header
        f.write("# LED Matrix Patterns\n")
        f.write("# Auto-generated from web drawings\n\n")
        f.write("PATTERNS = {\n")
        
        # Process each processed image
        for image_path in processed_images:
            print(f"Converting {os.path.basename(image_path)} to pattern...")
            
            # Convert image to pattern
            pattern_text = image_to_pattern(image_path)
            if pattern_text is None:
                continue
                
            # Write pattern to file
            f.write(pattern_text)
            f.write("\n\n")
        
        # Close the patterns dictionary
        f.write("}\n")
    
    print(f"\nPatterns saved to patterns/led_patterns.py")

def main():
    print("Starting image conversion...")
    convert_all_images()
    print("Conversion complete!")

if __name__ == "__main__":
    main()
