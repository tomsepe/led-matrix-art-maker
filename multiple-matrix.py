import board
import busio
from adafruit_ht16k33.matrix import Matrix8x8

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create an array of matrices
matrices = []
for i in range(3):
    # Initialize each matrix with a different address (0x70, 0x71, 0x72)
    matrix = Matrix8x8(i2c, address=0x70 + i)
    matrix.brightness = 1.0  # Set brightness (0.0 to 1.0)
    matrices.append(matrix)

# Example of controlling different matrices
matrices[0].pixel[0, 0] = 1  # Turn on pixel at (0,0) on first matrix
matrices[1].fill(1)          # Fill all pixels on second matrix
matrices[2].pixel[7, 7] = 1  # Turn on pixel at (7,7) on third matrix

# Don't forget to show the changes
for matrix in matrices:
    matrix.show()