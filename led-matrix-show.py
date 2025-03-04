import board
from adafruit_ht16k33.matrix import Matrix8x8
from PIL import Image
import os
import glob
import time
import argparse
import random

# Initialize I2C
i2c = board.I2C()

# Create three matrix objects with different I2C addresses
# Typical addresses are 0x70, 0x71, 0x72, but verify your actual addresses
matrix1 = Matrix8x8(i2c, address=0x72)  # Right matrix (was Left)
matrix2 = Matrix8x8(i2c, address=0x71)  # Middle matrix (unchanged)
matrix3 = Matrix8x8(i2c, address=0x70)  # Left matrix (was Right)

# Set brightness for all matrices (0.0 to 1.0)
BRIGHTNESS = 0.5
for matrix in [matrix1, matrix2, matrix3]:
    matrix.brightness = BRIGHTNESS
    matrix.blink_rate = 0  # Disable blinking

def display_image(image_path):
    """Load and display an image on the LED matrices"""
    image = Image.open(image_path)
    
    # Verify image dimensions (allowing both orientations)
    if image.size not in [(24, 8), (8, 24)]:
        print(f"Skipping {image_path}: Invalid dimensions {image.size}")
        return False
    
    # Rotate image if needed to get 24x8
    if image.size == (8, 24):
        image = image.rotate(90, expand=True)
    
    # Split the image into three 8x8 sections and display on each matrix
    right_section = image.crop((0, 0, 8, 8))    # Display on matrix1 (0x72)
    middle_section = image.crop((8, 0, 16, 8))  # Display on matrix2 (0x71)
    left_section = image.crop((16, 0, 24, 8))   # Display on matrix3 (0x70)
    
    # Display the sections on their respective matrices
    matrix1.image(right_section)  # Right matrix shows left section
    matrix2.image(middle_section) # Middle matrix shows middle section
    matrix3.image(left_section)   # Left matrix shows right section
    return True

def get_image_files():
    """Get list of 8x24 image files"""
    image_files = glob.glob("images/pixel_art_*8x24*.png")
    if not image_files:
        print("No 8x24 image files found in 'images' directory")
        return None
    return sorted(image_files)

def display_static():
    """Display the most recent image"""
    image_files = get_image_files()
    if not image_files:
        return
    
    # Get most recent file
    latest_image = max(image_files, key=os.path.getctime)
    print(f"Displaying {os.path.basename(latest_image)}")
    display_image(latest_image)

def display_loop():
    """Loop through all images"""
    DISPLAY_TIME = 3  # seconds to display each image
    
    while True:  # Loop forever
        image_files = get_image_files()
        if not image_files:
            time.sleep(5)  # Wait 5 seconds before checking again
            continue
        
        # Display each image in sequence
        for image_path in image_files:
            print(f"Displaying {os.path.basename(image_path)}")
            if display_image(image_path):
                time.sleep(DISPLAY_TIME)

def get_8x8_image_files():
    """Get list of 8x8 image files"""
    image_files = glob.glob("images/pixel_art_*8x8*.png")
    if not image_files:
        print("No 8x8 image files found in 'images' directory")
        return None
    return sorted(image_files)

def display_random_singles():
    """Display random 8x8 images on each matrix independently"""
    matrices = [matrix1, matrix2, matrix3]
    display_times = [1, 2, 3, 4, 5]  # Possible display durations in seconds
    next_change = [0, 0, 0]  # Next change time for each matrix
    
    while True:
        image_files = get_8x8_image_files()
        if not image_files:
            time.sleep(5)  # Wait 5 seconds before checking again
            continue
        
        current_time = time.time()
        
        # Check each matrix
        for i, matrix in enumerate(matrices):
            if current_time >= next_change[i]:
                # Choose random image and display time
                image_path = random.choice(image_files)
                display_time = random.choice(display_times)
                
                # Load and display image
                try:
                    image = Image.open(image_path)
                    if image.size == (8, 8):
                        matrix.image(image)
                        print(f"Matrix {i+1}: Displaying {os.path.basename(image_path)} for {display_time}s")
                    else:
                        print(f"Skipping {image_path}: Invalid dimensions {image.size}")
                except Exception as e:
                    print(f"Error displaying {image_path}: {e}")
                
                # Set next change time
                next_change[i] = current_time + display_time
        
        time.sleep(0.1)  # Small delay to prevent busy-waiting

def main():
    parser = argparse.ArgumentParser(description='Display images on LED matrix')
    parser.add_argument('mode', choices=['static', 'loop', 'single'],
                       help='static: display most recent image, '
                            'loop: cycle through all images, '
                            'single: random 8x8 images on each matrix')
    
    args = parser.parse_args()
    
    if args.mode == 'static':
        display_static()
    elif args.mode == 'single':
        display_random_singles()
    else:  # loop mode
        display_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting display")
