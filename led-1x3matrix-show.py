"""
LED Matrix Display Script (3x Matrix Version)

This script displays pixel art patterns on three 8x8 LED matrix displays.
It reads patterns from patterns/led_patterns.py and displays them randomly
on each matrix independently.

Features:
- Controls three 8x8 LED matrices simultaneously
- Each matrix displays patterns independently
- Random pattern selection and timing (1-5 seconds)
- Adjustable brightness (default 50%)
- Synchronized updates across all matrices
- Runs continuously until interrupted with Ctrl+C

Hardware:
- Uses three Adafruit HT16K33 8x8 LED Matrices
- Connected via I2C with addresses:
  - Left matrix: 0x70
  - Middle matrix: 0x71
  - Right matrix: 0x72
- Requires adafruit-circuitpython-ht16k33 library
"""

import board
from adafruit_ht16k33.matrix import Matrix8x8
import os
import time
import argparse
import random
from patterns.led_patterns import PATTERNS

# Initialize I2C
i2c = board.I2C()

# Create three matrix objects with different I2C addresses
# Typical addresses are 0x70, 0x71, 0x72, but verify your actual addresses
matrix1 = Matrix8x8(i2c, address=0x72)  # Right matrix
matrix2 = Matrix8x8(i2c, address=0x71)  # Middle matrix
matrix3 = Matrix8x8(i2c, address=0x70)  # Left matrix 

# Set brightness for all matrices (0.0 to 1.0)
BRIGHTNESS = 1.0  # Increased brightness for better visibility
for matrix in [matrix1, matrix2, matrix3]:
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
    matrices = [matrix1, matrix2, matrix3]
    display_times = [1, 2, 3, 4, 5]  # Possible display durations in seconds
    next_change = [0, 0, 0]  # Next change time for each matrix
    current_patterns = [None, None, None]  # Track current patterns
    
    print("Displaying random patterns. Press Ctrl+C to exit.")
    
    while True:
        pattern_names = get_pattern_names()
        if not pattern_names:
            print("No patterns available")
            time.sleep(5)  # Wait 5 seconds before checking again
            continue
        
        current_time = time.time()
        update_needed = False
        
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
                        current_patterns[i] = pattern_name
                        update_needed = True
                except Exception as e:
                    print(f"Error with pattern {pattern_name}: {e}")
                
                # Set next change time
                next_change[i] = current_time + display_time
        
        # Show all updates at once
        if update_needed:
            for matrix in matrices:
                matrix.show()
        
        time.sleep(0.05)  # Reduced delay for more responsive updates

def main():
    print("Starting LED Matrix Display...")
    try:
        display_random_patterns()
    except KeyboardInterrupt:
        print("\nExiting display")

if __name__ == "__main__":
    main()
