# pylint: disable=import-error,no-member
# For use with adafruit KB2040 board
#  SPDX-FileCopyrightText: 2021-2023 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython LED Matrix Display Script for 6 Matrices"""
import board
import busio
import time
import random
from adafruit_ht16k33.matrix import Matrix8x8
from patterns.led_patterns import PATTERNS

print("\nLED Matrix Display - 6 Matrix Setup")
print("=================================")

# Initialize both I2C buses
print("Initializing I2C buses...")
i2c1 = busio.I2C(board.A1, board.A0)  # First set of matrices
i2c2 = busio.I2C(board.A3, board.A2)  # Second set of matrices
print("I2C buses initialized successfully")

# Initialize matrices on first bus (A1/A0)
print("\nInitializing first set of matrices...")
matrices1 = []
for addr in [0x70, 0x71, 0x72]:
    try:
        matrix = Matrix8x8(i2c1, address=addr)
        matrix.brightness = 1.0  # Maximum brightness
        matrix.blink_rate = 0    # Disable blinking
        matrices1.append(matrix)
        print(f"Matrix at {hex(addr)} initialized successfully")
    except Exception as e:
        print(f"Error initializing matrix at {hex(addr)}: {e}")

# Initialize matrices on second bus (A3/A2)
print("\nInitializing second set of matrices...")
matrices2 = []
for addr in [0x70, 0x71, 0x72]:
    try:
        matrix = Matrix8x8(i2c2, address=addr)
        matrix.brightness = 1.0  # Maximum brightness
        matrix.blink_rate = 0    # Disable blinking
        matrices2.append(matrix)
        print(f"Matrix at {hex(addr)} initialized successfully")
    except Exception as e:
        print(f"Error initializing matrix at {hex(addr)}: {e}")

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
    bus1_matrices = matrices1
    bus2_matrices = matrices2
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

try:
    display_random_patterns()
except KeyboardInterrupt:
    print("\nStopping pattern display...")
finally:
    # Cleanup
    print("\nCleaning up displays...")
    for matrix in matrices1 + matrices2:
        try:
            matrix.fill(0)  # Clear display
        except:
            pass
    
    try:
        i2c1.deinit()
        i2c2.deinit()
        print("I2C buses deinitialized successfully")
    except Exception as e:
        print(f"Error during cleanup: {e}")

print("\nDisplay test complete!")
