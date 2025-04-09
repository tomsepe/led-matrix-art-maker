# pylint: disable=import-error,no-member
# For use with adafruit KB2040 board
#  SPDX-FileCopyrightText: 2021-2023 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython LED Matrix Display Script for 6 Matrices"""
import board
import busio
import time
from adafruit_ht16k33 import segments

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
        matrix = segments.Seg7x4(i2c1, address=addr)
        matrices1.append(matrix)
        print(f"Matrix at {hex(addr)} initialized successfully")
    except Exception as e:
        print(f"Error initializing matrix at {hex(addr)}: {e}")

# Initialize matrices on second bus (A3/A2)
print("\nInitializing second set of matrices...")
matrices2 = []
for addr in [0x70, 0x71, 0x72]:
    try:
        matrix = segments.Seg7x4(i2c2, address=addr)
        matrices2.append(matrix)
        print(f"Matrix at {hex(addr)} initialized successfully")
    except Exception as e:
        print(f"Error initializing matrix at {hex(addr)}: {e}")

# Test patterns for display
test_patterns = [
    "8888",  # All segments
    "----",  # Middle segments
    "0000",  # Outer segments
    "9999",  # Most segments
    "1234",  # Numbers
    "5678",  # Numbers
    "ABCD",  # Letters
    "EFGH",  # Letters
]

def display_patterns():
    """Display test patterns on all matrices"""
    print("\nStarting pattern display...")
    try:
        while True:
            for pattern in test_patterns:
                print(f"\nDisplaying pattern: {pattern}")
                
                # Display on first set of matrices
                for i, matrix in enumerate(matrices1):
                    try:
                        matrix.print(pattern)
                        print(f"Bus 1, Matrix {i+1}: {pattern}")
                    except Exception as e:
                        print(f"Error on Bus 1, Matrix {i+1}: {e}")
                
                # Display on second set of matrices
                for i, matrix in enumerate(matrices2):
                    try:
                        matrix.print(pattern)
                        print(f"Bus 2, Matrix {i+1}: {pattern}")
                    except Exception as e:
                        print(f"Error on Bus 2, Matrix {i+1}: {e}")
                
                time.sleep(2)  # Display each pattern for 2 seconds
                
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

# Start the display
display_patterns()

print("\nDisplay test complete!")
