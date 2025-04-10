"""
Convert high-resolution images to low-resolution 8x8 versions.

This script reads PNG files from the 'saved-drawings' directory,
resizes them to 8x8 pixels, and saves them in the 'image-data' directory.
Uses the same naming convention as bit-draw.py:
- High-res: pixel_art_{timestamp}.png
- Low-res: pixel_art_{timestamp}_{width}x{height}.png
"""

import os
from PIL import Image
from datetime import datetime

# Create directories if they don't exist
os.makedirs('saved-drawings', exist_ok=True)
os.makedirs('image-data', exist_ok=True)

def convert_image(input_path, output_path):
    """Convert a single image to 8x8 resolution."""
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to 8x8
            img_resized = img.resize((8, 8), Image.Resampling.LANCZOS)
            
            # Save the resized image
            img_resized.save(output_path)
            print(f"Converted: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
            return True
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return False

def main():
    # Get list of PNG files in saved-drawings
    input_files = [f for f in os.listdir('saved-drawings') if f.lower().endswith('.png')]
    
    if not input_files:
        print("No PNG files found in 'saved-drawings' directory.")
        return
    
    print(f"Found {len(input_files)} PNG files to convert.")
    
    # Convert each file
    success_count = 0
    for input_file in input_files:
        input_path = os.path.join('saved-drawings', input_file)
        
        # Extract timestamp from filename (assuming format pixel_art_TIMESTAMP.png)
        try:
            # Remove 'pixel_art_' prefix and '.png' suffix
            timestamp = input_file[10:-4]
        except IndexError:
            print(f"Skipping {input_file}: Invalid filename format")
            continue
            
        # Create output filename with correct format
        output_path = os.path.join('image-data', f"pixel_art_{timestamp}_8x8.png")
        
        if convert_image(input_path, output_path):
            success_count += 1
    
    print(f"\nConversion complete. Successfully converted {success_count} out of {len(input_files)} files.")

if __name__ == "__main__":
    main()
