import board
from adafruit_ht16k33.matrix import Matrix8x8
from PIL import Image

# Initialize I2C
i2c = board.I2C()

# Create three matrix objects with different I2C addresses
# Typical addresses are 0x70, 0x71, 0x72, but verify your actual addresses
matrix1 = Matrix8x8(i2c, address=0x70)
matrix2 = Matrix8x8(i2c, address=0x71)
matrix3 = Matrix8x8(i2c, address=0x72)

# Set brightness for all matrices (0.0 to 1.0)
matrix1.brightness = 0.5
matrix2.brightness = 0.5
matrix3.brightness = 0.5

# Optional: Set blink rate for all matrices
matrix1.blink_rate = 0
matrix2.blink_rate = 0
matrix3.blink_rate = 0

# If you want to display an image across all three matrices
# You'll need an image that's 24x8 pixels (3 matrices × 8 pixels wide)
image = Image.open("drawings/pixel-art-001.png")

# Split the image into three 8x8 sections and display on each matrix
# Assuming your image is 24x8 pixels
left_section = image.crop((0, 0, 8, 8))
middle_section = image.crop((8, 0, 16, 8))
right_section = image.crop((16, 0, 24, 8))

matrix1.image(left_section)
matrix2.image(middle_section)
matrix3.image(right_section)

# Example of setting individual pixels on each matrix
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
