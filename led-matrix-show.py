import board
import busio
from adafruit_ht16k33.matrix import Matrix8x8
import time
import random
from patterns.led_patterns import PATTERNS

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Create three matrix objects with different I2C addresses
matrix1 = Matrix8x8(i2c, address=0x72)  # Right matrix
matrix2 = Matrix8x8(i2c, address=0x71)  # Middle matrix
matrix3 = Matrix8x8(i2c, address=0x70)  # Left matrix

# Set brightness for all matrices (0.0 to 1.0)
BRIGHTNESS = 0.5
for matrix in [matrix1, matrix2, matrix3]:
    matrix.brightness = BRIGHTNESS
    matrix.blink_rate = 0  # Disable blinking

def display_pattern(matrix, pattern_data):
    """Display an 8x8 pattern on a single matrix"""
    try:
        # Clear the matrix first
        matrix.fill(0)
        # Display each row of the pattern
        for row, byte_val in enumerate(pattern_data):
            # Convert each bit in the byte to pixels
            for col in range(8):
                pixel_val = (byte_val >> (7 - col)) & 1
                matrix[col, row] = pixel_val
        matrix.show()
        return True
    except Exception as e:
        print(f"Error displaying pattern: {e}")
        return False

def get_pattern_names():
    """Get list of available pattern names"""
    return sorted(PATTERNS.keys())

def main():
    print("Starting LED Matrix Display...")
    
    # Get list of patterns once at startup
    pattern_names = get_pattern_names()
    if not pattern_names:
        print("No patterns available!")
        return
        
    matrices = [matrix1, matrix2, matrix3]
    next_change = [0, 0, 0]  # Next change time for each matrix
    
    while True:
        current_time = time.monotonic()  # Use monotonic time for CircuitPython
        
        # Check each matrix
        for i, matrix in enumerate(matrices):
            if current_time >= next_change[i]:
                # Choose random pattern and display time (1-5 seconds)
                pattern_name = random.choice(pattern_names)
                display_time = random.randint(1, 5)
                
                try:
                    # Get and display the pattern
                    pattern_data = PATTERNS[pattern_name]
                    if display_pattern(matrix, pattern_data):
                        print(f"Matrix {i+1}: {pattern_name}")
                except Exception as e:
                    print(f"Error: {e}")
                
                # Set next change time
                next_change[i] = current_time + display_time
        
        # Small delay to prevent busy-waiting
        time.sleep(0.1)

if __name__ == "__main__":
    main()
