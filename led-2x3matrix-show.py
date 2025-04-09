"""
LED Matrix Display Script (6x Matrix Version)

This script displays pixel art patterns on six 8x8 LED matrix displays,
using two separate I2C buses. It reads patterns from patterns/led_patterns.py
and displays them randomly on each matrix independently.

Features:
- Controls six 8x8 LED matrices simultaneously
- Uses two separate I2C buses for better performance
- Each matrix displays patterns independently
- Random pattern selection and timing (1-5 seconds)
- Adjustable brightness (default 100%)
- Synchronized updates across all matrices
- Runs continuously until interrupted with Ctrl+C

Hardware:
- Uses six Adafruit HT16K33 8x8 LED Matrices
- Connected via two I2C buses:
  Bus 1 (Primary):
  - Left matrix: 0x70
  - Middle matrix: 0x71
  - Right matrix: 0x72
  Bus 2 (Secondary):
  - Left matrix: 0x70
  - Middle matrix: 0x71
  - Right matrix: 0x72
- Requires adafruit-circuitpython-ht16k33 library
"""

import board
import busio
from adafruit_ht16k33.matrix import Matrix8x8
import os
import time
import random
from patterns.led_patterns import PATTERNS

# Initialize both I2C buses
i2c1 = board.I2C()  # Primary I2C bus (default)
i2c2 = busio.I2C(board.SDA_1, board.SCL_1)  # Secondary I2C bus using hardware I2C port 1

# Create matrix objects for first set (Bus 1)
matrix1_1 = Matrix8x8(i2c1, address=0x72)  # Right matrix
matrix1_2 = Matrix8x8(i2c1, address=0x71)  # Middle matrix
matrix1_3 = Matrix8x8(i2c1, address=0x70)  # Left matrix

# Create matrix objects for second set (Bus 2)
matrix2_1 = Matrix8x8(i2c2, address=0x72)  # Right matrix
matrix2_2 = Matrix8x8(i2c2, address=0x71)  # Middle matrix
matrix2_3 = Matrix8x8(i2c2, address=0x70)  # Left matrix

# Set brightness for all matrices (0.0 to 1.0)
BRIGHTNESS = 1.0  # Maximum brightness for optimal visibility
for matrix in [matrix1_1, matrix1_2, matrix1_3, matrix2_1, matrix2_2, matrix2_3]:
    matrix.brightness = BRIGHTNESS
    matrix.blink_rate = 0  # Disable blinking

def display_pattern(matrix, pattern_data):
    """Display an 8x8 pattern on a single matrix using optimized methods"""
    try:
        # First clear the matrix using fill() which is faster than setting individual pixels
        matrix.fill(0)
        
        # Set pixels using direct buffer manipulation
        for row, byte_val in enumerate(pattern_data):
            for col in range(8):
                if (byte_val >> (7 - col)) & 1:
                    matrix.pixel(col, row, 1)
        return True
    except Exception as e:
        print(f"Error displaying pattern: {e}")
        return False

def get_pattern_names():
    """Get list of available pattern names"""
    return sorted(PATTERNS.keys())

def display_random_patterns():
    """Display random patterns on each matrix independently"""
    # Group matrices by bus for better organization
    bus1_matrices = [matrix1_1, matrix1_2, matrix1_3]
    bus2_matrices = [matrix2_1, matrix2_2, matrix2_3]
    all_matrices = bus1_matrices + bus2_matrices
    
    display_times = [1, 2, 3, 4, 5]  # Possible display durations in seconds
    next_change = [0] * 6  # Next change time for each matrix
    current_patterns = [None] * 6  # Track current patterns
    
    print("Displaying random patterns on 6 matrices. Press Ctrl+C to exit.")
    
    while True:
        pattern_names = get_pattern_names()
        if not pattern_names:
            print("No patterns available")
            time.sleep(5)  # Wait 5 seconds before checking again
            continue
        
        current_time = time.time()
        update_needed = False
        
        # Check each matrix
        for i, matrix in enumerate(all_matrices):
            if current_time >= next_change[i]:
                # Choose random pattern and display time
                pattern_name = random.choice(pattern_names)
                display_time = random.choice(display_times)
                
                try:
                    # Get and display the pattern
                    pattern_data = PATTERNS[pattern_name]
                    if display_pattern(matrix, pattern_data):
                        bus_num = 1 if i < 3 else 2
                        matrix_num = (i % 3) + 1
                        print(f"Bus {bus_num}, Matrix {matrix_num}: Displaying {pattern_name} for {display_time}s")
                        current_patterns[i] = pattern_name
                        update_needed = True
                except Exception as e:
                    print(f"Error with pattern {pattern_name}: {e}")
                
                # Set next change time
                next_change[i] = current_time + display_time
        
        # Show all updates at once, grouped by bus
        if update_needed:
            for matrix in bus1_matrices:
                matrix.show()
            for matrix in bus2_matrices:
                matrix.show()
        
        time.sleep(0.05)  # Reduced delay for more responsive updates

def main():
    print("Starting 6x LED Matrix Display...")
    try:
        display_random_patterns()
    except KeyboardInterrupt:
        print("\nExiting display")

if __name__ == "__main__":
    main()
