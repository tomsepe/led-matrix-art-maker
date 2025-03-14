import board
from adafruit_ht16k33.matrix import Matrix8x8
import os
import time
import argparse
import random
from patterns.led_patterns import PATTERNS

# Initialize I2C
i2c = board.I2C()
i2c.try_lock()
i2c.configure(frequency=400000)  # Set to 400kHz (fast mode)
i2c.unlock()

# Create three matrix objects with different I2C addresses
# Typical addresses are 0x70, 0x71, 0x72, but verify your actual addresses
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
        # Display each row of the pattern
        for row, byte_val in enumerate(pattern_data):
            # Convert each bit in the byte to pixels
            for col in range(8):
                matrix[col, row] = (byte_val >> (7 - col)) & 1
        matrix.show()
        return True
    except Exception as e:
        print(f"Error displaying pattern: {e}")
        return False

def get_pattern_names():
    """Get list of available pattern names"""
    return sorted(PATTERNS.keys())

def display_random_patterns():
    """Display random patterns on each matrix independently"""
    matrices = [matrix1, matrix2, matrix3]
    display_times = [1, 2, 3, 4, 5]  # Possible display durations in seconds
    next_change = [0, 0, 0]  # Next change time for each matrix
    
    print("Displaying random patterns. Press Ctrl+C to exit.")
    
    while True:
        pattern_names = get_pattern_names()
        if not pattern_names:
            print("No patterns available")
            time.sleep(5)  # Wait 5 seconds before checking again
            continue
        
        current_time = time.time()
        
        # Check each matrix
        for i, matrix in enumerate(matrices):
            if current_time >= next_change[i]:
                # Choose random pattern and display time
                pattern_name = random.choice(pattern_names)
                display_time = random.choice(display_times)
                
                try:
                    # Get and display the pattern
                    pattern_data = PATTERNS[pattern_name]
                    if display_pattern(matrix, pattern_data):
                        print(f"Matrix {i+1}: Displaying {pattern_name} for {display_time}s")
                except Exception as e:
                    print(f"Error with pattern {pattern_name}: {e}")
                
                # Set next change time
                next_change[i] = current_time + display_time
        
        time.sleep(0.1)  # Small delay to prevent busy-waiting

def main():
    print("Starting LED Matrix Display...")
    try:
        display_random_patterns()
    except KeyboardInterrupt:
        print("\nExiting display")

if __name__ == "__main__":
    main()
