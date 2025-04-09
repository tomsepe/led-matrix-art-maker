# pylint: disable=import-error,no-member
# For use with adafruit KB2040 board
#  SPDX-FileCopyrightText: 2021-2023 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython I2C possible pin-pair identifying script"""
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

# Test first I2C bus (default pins)
print("\nTesting first I2C bus (SCL/SDA)...")
try:
    i2c1 = busio.I2C(board.SCL, board.SDA)
    print("First bus initialized successfully")
    
    # Scan for devices
    print("Scanning for devices...")
    devices1 = i2c1.scan()
    if devices1:
        print("Found devices at addresses:", [hex(device) for device in devices1])
    else:
        print("No devices found on first bus")
    
    # Deinitialize first bus
    i2c1.deinit()
    print("First bus deinitialized")
except Exception as e:
    print(f"Error with first bus: {e}")

# Wait a moment between tests
time.sleep(1)

# Test second I2C bus (alternative pins)
print("\nTesting second I2C bus (A3/A2)...")
try:
    i2c2 = busio.I2C(board.A3, board.A2)
    print("Second bus initialized successfully")
    
    # Scan for devices
    print("Scanning for devices...")
    devices2 = i2c2.scan()
    if devices2:
        print("Found devices at addresses:", [hex(device) for device in devices2])
    else:
        print("No devices found on second bus")
    
    # Deinitialize second bus
    i2c2.deinit()
    print("Second bus deinitialized")
except Exception as e:
    print(f"Error with second bus: {e}")

print("\nI2C bus test complete!")
print("Press any key to enter the REPL")
