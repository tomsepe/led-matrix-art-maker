import board
from adafruit_ht16k33.matrix import Matrix8x8

i2c = board.I2C()
matrix = Matrix8x8(i2c)

matrix = Matrix8x8(i2c, address=0x71)

matrix.brightness = 0.5

matrix.blink_rate = 3

# Setting Individual Pixels
matrix[0, 0] = 1
matrix[4, 4] = 1
matrix[7, 7] = 1

# Filling a Row
matrix.fill_row(0, 1)

# Filling the Entire Matrix
matrix.fill(1)

# Clearing the Matrix
matrix.fill(0)

# Clearing a Row
matrix.fill_row(0, 0)

# Shifting the Matrix
matrix.shift(2, 0)	# shift pixels to the right by 2
matrix.shift(-1, 0)	# shift pixels to the left by 1
matrix.shift(0, -3)	# shift pixels down by 3
matrix.shift(-2, 2)	# shift pixels left by 2 and up by 2

#loop all the pixels that are shifted
matrix.shift(2, 0, True)	# loop pixels to the right by 2
matrix.shift(-1, 0, True)	# loop pixels to the left by 1
matrix.shift(0, -3, True)	# loop pixels down by 3
matrix.shift(-2, 2, True)	# loop pixels left by 2 and up by 2

# convenience functions
matrix.shift_up()		# Shift pixels up
matrix.shift_left()		# Shift pixels left
matrix.shift_down()		# Shift pixels down
matrix.shift_right()		# Shift pixels right
matrix.shift_up(True)		# Loop pixels up
matrix.shift_left(True)	# Loop pixels left
matrix.shift_down(True)	# Loop pixels down
matrix.shift_right(True)	# Loop pixels right

# displayiong an image
import board
from PIL import Image
from adafruit_ht16k33 import matrix

matrix = matrix.Matrix8x8(board.I2C())

image = Image.open("images/led_matrices_squares-mono-8x8.png")
matrix.image(image)
