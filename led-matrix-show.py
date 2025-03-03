import board
from adafruit_ht16k33.matrix import Matrix8x8
from PIL import Image

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

# Load the image (expecting 24x8 pixels - 3 matrices × 8 pixels wide)
image = Image.open("drawings/pixel-art-001.png")

# Verify image dimensions
if image.size != (24, 8):
    raise ValueError(f"Image must be 24x8 pixels, got {image.size}")

# Split the image into three 8x8 sections and display on each matrix
left_section = image.crop((0, 0, 8, 8))
middle_section = image.crop((8, 0, 16, 8))
right_section = image.crop((16, 0, 24, 8))

# Display the sections on their respective matrices
matrix1.image(left_section)
matrix2.image(middle_section)
matrix3.image(right_section)

# Example of setting individual pixels on each matrix (commented out)
"""
# Matrix 1 (leftmost)
matrix1[0, 0] = 1  # Top-left pixel
matrix1.fill(1)    # Fill all pixels

# Matrix 2 (middle)
matrix2[4, 4] = 1  # Middle pixel
matrix2.fill(1)    # Fill all pixels

# Matrix 3 (rightmost)
matrix3[7, 7] = 1  # Bottom-right pixel
matrix3.fill(1)    # Fill all pixels
"""
