import board
from adafruit_ht16k33.matrix import Matrix8x8
from PIL import Image
import os
import glob
import time

# Initialize I2C
i2c = board.I2C()

# Create three matrix objects with different I2C addresses
# Typical addresses are 0x70, 0x71, 0x72, but verify your actual addresses
matrix1 = Matrix8x8(i2c, address=0x70)  # Left matrix
matrix2 = Matrix8x8(i2c, address=0x71)  # Middle matrix
matrix3 = Matrix8x8(i2c, address=0x72)  # Right matrix

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
    left_section = image.crop((0, 0, 8, 8))
    middle_section = image.crop((8, 0, 16, 8))
    right_section = image.crop((16, 0, 24, 8))
    
    # Display the sections on their respective matrices
    matrix1.image(left_section)
    matrix2.image(middle_section)
    matrix3.image(right_section)
    return True

def main():
    DISPLAY_TIME = 3  # seconds to display each image
    
    while True:  # Loop forever
        # Get list of image files
        image_files = glob.glob("images/pixel_art_*.png")
        if not image_files:
            print("No image files found in 'images' directory")
            time.sleep(5)  # Wait 5 seconds before checking again
            continue
        
        # Sort files by name to ensure consistent order
        image_files.sort()
        
        # Display each image in sequence
        for image_path in image_files:
            print(f"Displaying {os.path.basename(image_path)}")
            if display_image(image_path):
                time.sleep(DISPLAY_TIME)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting slideshow")
