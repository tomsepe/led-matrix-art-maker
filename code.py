# pylint: disable=import-error,no-member
# For use with adafruit KB2040 board
#  SPDX-FileCopyrightText: 2021-2023 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython I2C bus testing script"""
import board
import busio
from microcontroller import Pin
import time
from adafruit_ht16k33 import segments

def is_hardware_i2c(scl, sda):
    try:
        p = busio.I2C(scl, sda)
        p.deinit()
        return True
    except ValueError:
        return False
    except RuntimeError:
        return True


def get_unique_pins():
    exclude = [
        getattr(board, p)
        for p in [
            # This is not an exhaustive list of unexposed pins. Your results
            # may include other pins that you cannot easily connect to.
            "NEOPIXEL",
            "DOTSTAR_CLOCK",
            "DOTSTAR_DATA",
            "APA102_SCK",
            "APA102_MOSI",
            "LED",
            "SWITCH",
            "BUTTON",
            "ACCELEROMETER_INTERRUPT",
            "VOLTAGE_MONITOR",
            "MICROPHONE_CLOCK",
            "MICROPHONE_DATA",
            "RFM_RST",
            "RFM_CS",
            "RFM_IO0",
            "RFM_IO1",
            "RFM_IO2",
            "RFM_IO3",
            "RFM_IO4",
            "RFM_IO5",
            "TFT_I2C_POWER",
            "NEOPIXEL_POWER",
        ]
        if p in dir(board)
    ]
    pins = [
        pin
        for pin in [getattr(board, p) for p in dir(board)]
        if isinstance(pin, Pin) and pin not in exclude
    ]
    unique = []
    for p in pins:
        if p not in unique:
            unique.append(p)
    return unique

# Test I2C pin pairs and store results
valid_pairs = []
for scl_pin in get_unique_pins():
    for sda_pin in get_unique_pins():
        if scl_pin is sda_pin:
            continue
        if is_hardware_i2c(scl_pin, sda_pin):
            valid_pairs.append((scl_pin, sda_pin))

# Print results to REPL
print("\nI2C Pin Pair Test Results")
print("========================")
for scl, sda in valid_pairs:
    print(f"SCL pin: {scl}\t SDA pin: {sda}")
print(f"\nFound {len(valid_pairs)} valid I2C pin pairs")

# I2C Bus Test for KB2040
# Tests two separate I2C buses for LED matrix control

print("\nI2C Bus Test for KB2040")
print("======================")

def test_i2c_bus(scl_pin, sda_pin, bus_name):
    print(f"\nTesting {bus_name} I2C bus ({scl_pin}/{sda_pin})...")
    i2c = None
    try:
        # Initialize I2C bus
        i2c = busio.I2C(scl_pin, sda_pin)
        print(f"{bus_name} bus initialized successfully")
        
        # Wait for I2C lock
        while not i2c.try_lock():
            pass
        
        # Scan for devices
        print("Scanning for devices...")
        devices = i2c.scan()
        if devices:
            print("Found devices at addresses:", [hex(device) for device in devices])
        else:
            print("No devices found")
        
        # Release I2C lock
        i2c.unlock()
        
    except Exception as e:
        print(f"Error with {bus_name} bus: {e}")
    finally:
        # Ensure I2C is properly deinitialized
        if i2c:
            try:
                i2c.deinit()
                print(f"{bus_name} bus deinitialized")
            except:
                pass
        time.sleep(1)  # Wait between tests

# Test first I2C bus (default pins)
test_i2c_bus(board.SCL, board.SDA, "First")

# Test second I2C bus (alternative pins)
test_i2c_bus(board.A3, board.A2, "Second")

print("\nI2C bus test complete!")
print("Press any key to enter the REPL")
