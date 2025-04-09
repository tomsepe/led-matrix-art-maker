# For use with adafruit KB2040 board
#  SPDX-FileCopyrightText: 2021-2023 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython I2C possible pin-pair identifying script"""
import board
import busio
from microcontroller import Pin
import time

print("Starting I2C pin pair test...")
print("This may take a few moments...")

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
    print("Getting available pins...")
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
    print(f"Found {len(unique)} available pins")
    return unique

print("\nTesting I2C pin pairs...")
print("Valid pairs will be listed below:")
print("-------------------------------")

valid_pairs = []
for scl_pin in get_unique_pins():
    for sda_pin in get_unique_pins():
        if scl_pin is sda_pin:
            continue
        if is_hardware_i2c(scl_pin, sda_pin):
            result = f"SCL pin: {scl_pin}\t SDA pin: {sda_pin}"
            print(result)
            valid_pairs.append((scl_pin, sda_pin))

print("\nTest complete!")
print(f"Found {len(valid_pairs)} valid I2C pin pairs")
print("\nPress Ctrl+C to exit")

# Simple LED blink test
led = board.LED

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
