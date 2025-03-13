#!/usr/bin/env python3

from PIL import Image
import os
import glob
from datetime import datetime

def ensure_directories():
    """Create necessary directories if they don't exist"""
    for directory in ['bytes']:
        if not os.path.exists(directory):
            os.makedirs(directory)

def image_to_bytes(image_path):
    """Convert an image to LED matrix byte format"""
    try:
        # Open and verify image
        image = Image.open(image_path)
        
        # Handle different image sizes
        if image.size == (8, 24):
            image = image.rotate(90, expand=True)
        elif image.size == (8, 8):
            # For 8x8 images, create a 24x8 image with the pattern repeated
            new_image = Image.new('RGB', (24, 8), 'black')
            for i in range(3):  # Repeat the pattern 3 times
                new_image.paste(image, (i * 8, 0))
            image = new_image
        elif image.size != (24, 8):
            print(f"Skipping {image_path}: Invalid dimensions {image.size}")
            return None
            
        # Convert to black and white
        image = image.convert('L')  # Convert to grayscale
        
        # Create byte array for the image
        byte_array = []
        
        # Process each 8x8 matrix section
        for matrix_start_x in range(0, 24, 8):
            # Process each row in the matrix
            for y in range(8):
                byte_val = 0
                # Process each pixel in the row
                for x in range(8):
                    pixel = image.getpixel((matrix_start_x + x, y))
                    # Convert pixel to bit (white = 1, black = 0)
                    bit = 1 if pixel > 127 else 0
                    byte_val |= (bit << (7 - x))
                byte_array.append(byte_val)
        
        return bytes(byte_array)
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def convert_all_images():
    """Convert all PNG images in images directory to byte format"""
    ensure_directories()
    
    # Get all PNG files
    image_files = glob.glob("images/pixel_art_*.png")
    if not image_files:
        print("No image files found in 'images' directory")
        return
    
    print(f"Found {len(image_files)} images to convert")
    
    # Process each image
    for image_path in image_files:
        print(f"Converting {os.path.basename(image_path)}...")
        
        # Convert image to bytes
        byte_data = image_to_bytes(image_path)
        if byte_data is None:
            continue
            
        # Extract timestamp from original filename
        # Format is pixel_art_YYYYMMDD_HHMMSS_WxH.png
        try:
            base_name = os.path.basename(image_path)
            name_parts = base_name.split('_')  # Split on underscores
            timestamp = f"{name_parts[2]}_{name_parts[3]}"  # Combine date and time parts
            
            # Remove dimensions and .png from timestamp if present
            timestamp = timestamp.split('_')[0] + '_' + timestamp.split('_')[1].split('.')[0]
            
        except Exception as e:
            print(f"Error extracting timestamp from {base_name}, using current time: {e}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
        byte_filename = f"bytes/pixel_art_{timestamp}.bytes"
        
        # Save byte data
        with open(byte_filename, 'wb') as f:
            f.write(byte_data)
        print(f"Saved as {byte_filename}")

def main():
    print("Starting image conversion...")
    convert_all_images()
    print("Conversion complete!")

if __name__ == "__main__":
    main()
