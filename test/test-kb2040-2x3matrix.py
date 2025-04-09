# pylint: disable=import-error,no-member
# For use with adafruit KB2040 board
#  SPDX-FileCopyrightText: 2021-2023 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython I2C bus diagnostic script for both matrix sets"""
import board
import busio
import time
from adafruit_ht16k33 import segments

print("\nLED Matrix Diagnostic - Both Sets")
print("===============================")

def test_matrix_set(scl_pin, sda_pin, set_name):
    print(f"\nTesting {set_name} matrix set ({scl_pin}/{sda_pin})...")
    
    i2c = None
    matrices = []
    try:
        # Initialize I2C bus
        print("Initializing I2C bus...")
        i2c = busio.I2C(scl_pin, sda_pin)
        print("I2C bus initialized successfully")
        
        # Wait for I2C lock
        print("Waiting for I2C lock...")
        while not i2c.try_lock():
            pass
        print("I2C lock acquired")
        
        # Scan for devices
        print("\nScanning for devices...")
        devices = i2c.scan()
        if devices:
            print("Found devices at addresses:", [hex(device) for device in devices])
            
            # Release lock before initializing matrices
            i2c.unlock()
            print("I2C lock released for matrix initialization")
            
            # Initialize matrices
            print("\nInitializing matrices...")
            for addr in devices:
                try:
                    print(f"Attempting to initialize matrix at {hex(addr)}...")
                    matrix = segments.Seg7x4(i2c, address=addr)
                    matrices.append(matrix)
                    print(f"Matrix at {hex(addr)} initialized successfully")
                except Exception as e:
                    print(f"Error initializing matrix at {hex(addr)}: {e}")
            
            # Test each matrix
            if matrices:
                print("\nTesting matrix display...")
                test_patterns = ["8888", "----", "0000", "9999"]
                for i, matrix in enumerate(matrices):
                    print(f"\nTesting matrix {i+1}:")
                    # Test each pattern
                    for pattern in test_patterns:
                        try:
                            matrix.print(pattern)
                            print(f"Displaying: {pattern}")
                            time.sleep(1)
                        except Exception as e:
                            print(f"Error displaying pattern {pattern}: {e}")
                    matrix.fill(0)  # Clear display
                    
        else:
            print("No devices found on this bus")
            try:
                i2c.unlock()
            except:
                pass
        
    except Exception as e:
        print(f"\nError during test: {e}")
        print("Please check:")
        print("1. Physical connections")
        print("2. Power supply")
        print("3. Pin conflicts with other peripherals")
        
    finally:
        # Cleanup
        if matrices:
            print("\nCleaning up matrices...")
            for matrix in matrices:
                try:
                    matrix.fill(0)  # Clear display
                except:
                    pass
        
        if i2c:
            try:
                # Try to unlock first
                try:
                    i2c.unlock()
                except:
                    pass
                # Then deinit
                i2c.deinit()
                print("I2C bus deinitialized successfully")
            except Exception as e:
                print(f"Error during I2C deinitialization: {e}")
        time.sleep(1)

# Test first set of matrices (A1/A0)
test_matrix_set(board.A1, board.A0, "First")

# Test second set of matrices (A3/A2)
test_matrix_set(board.A3, board.A2, "Second")

print("\nDiagnostic test complete!")
