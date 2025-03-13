import board
from adafruit_ht16k33.matrix import Matrix8x8
import os
import glob
import time
import argparse
import random

# Initialize I2C
i2c = board.I2C()

# Create three matrix objects with different I2C addresses
# Typical addresses are 0x70, 0x71, 0x72, but verify your actual addresses
matrix1 = Matrix8x8(i2c, address=0x72)  # Right matrix (was Left)
matrix2 = Matrix8x8(i2c, address=0x71)  # Middle matrix (unchanged)
matrix3 = Matrix8x8(i2c, address=0x70)  # Left matrix (was Right)

# Set brightness for all matrices (0.0 to 1.0)
BRIGHTNESS = 0.5
for matrix in [matrix1, matrix2, matrix3]:
    matrix.brightness = BRIGHTNESS
    matrix.blink_rate = 0  # Disable blinking

def display_bytes(byte_path):
    """Load and display bytes on the LED matrices"""
    try:
        with open(byte_path, 'rb') as f:
            data = f.read()
        
        # Each 8x8 matrix needs 8 bytes (one byte per row)
        # For 3 matrices we need 24 bytes total
        if len(data) != 24:
            print(f"Skipping {byte_path}: Invalid data length {len(data)}")
            return False
        
        # Split the bytes into three 8-byte sections for each matrix
        right_data = data[0:8]     # First 8 bytes for matrix1 (0x72)
        middle_data = data[8:16]   # Next 8 bytes for matrix2 (0x71)
        left_data = data[16:24]    # Last 8 bytes for matrix3 (0x70)
        
        # Display the data on each matrix
        for i, row in enumerate(right_data):
            matrix1.pixel = row  # Set entire row using byte value
        for i, row in enumerate(middle_data):
            matrix2.pixel = row
        for i, row in enumerate(left_data):
            matrix3.pixel = row
            
        return True
    except Exception as e:
        print(f"Error displaying {byte_path}: {e}")
        return False

def get_byte_files():
    """Get list of byte files"""
    byte_files = glob.glob("bytes/pixel_art_*.bytes")
    if not byte_files:
        print("No byte files found in 'bytes' directory")
        return None
    return sorted(byte_files)

def display_static():
    """Display the most recent byte file"""
    byte_files = get_byte_files()
    if not byte_files:
        return
    
    # Get most recent file
    latest_file = max(byte_files, key=os.path.getctime)
    print(f"Displaying {os.path.basename(latest_file)}")
    display_bytes(latest_file)

def display_loop():
    """Loop through all byte files"""
    DISPLAY_TIME = 3  # seconds to display each file
    
    while True:  # Loop forever
        byte_files = get_byte_files()
        if not byte_files:
            time.sleep(5)  # Wait 5 seconds before checking again
            continue
        
        # Display each file in sequence
        for byte_path in byte_files:
            print(f"Displaying {os.path.basename(byte_path)}")
            if display_bytes(byte_path):
                time.sleep(DISPLAY_TIME)

def get_8x8_byte_files():
    """Get list of single matrix (8 byte) files"""
    # For future use if we implement single matrix byte files
    return get_byte_files()

def display_random_singles():
    """Display random sections from byte files on each matrix independently"""
    matrices = [matrix1, matrix2, matrix3]
    display_times = [1, 2, 3, 4, 5]  # Possible display durations in seconds
    next_change = [0, 0, 0]  # Next change time for each matrix
    
    while True:
        byte_files = get_byte_files()
        if not byte_files:
            time.sleep(5)  # Wait 5 seconds before checking again
            continue
        
        current_time = time.time()
        
        # Check each matrix
        for i, matrix in enumerate(matrices):
            if current_time >= next_change[i]:
                # Choose random file and display time
                byte_path = random.choice(byte_files)
                display_time = random.choice(display_times)
                
                # Load and display section
                try:
                    with open(byte_path, 'rb') as f:
                        data = f.read()
                    if len(data) == 24:  # Ensure we have complete data
                        # Select the appropriate 8-byte section for this matrix
                        section_start = i * 8
                        section_data = data[section_start:section_start + 8]
                        # Display the section
                        for row, byte_val in enumerate(section_data):
                            matrix.pixel = byte_val
                        print(f"Matrix {i+1}: Displaying section from {os.path.basename(byte_path)} for {display_time}s")
                except Exception as e:
                    print(f"Error displaying {byte_path}: {e}")
                
                # Set next change time
                next_change[i] = current_time + display_time
        
        time.sleep(0.1)  # Small delay to prevent busy-waiting

def main():
    parser = argparse.ArgumentParser(description='Display byte patterns on LED matrix')
    parser.add_argument('mode', choices=['static', 'loop', 'single'],
                       help='static: display most recent pattern, '
                            'loop: cycle through all patterns, '
                            'single: random sections on each matrix')
    
    args = parser.parse_args()
    
    if args.mode == 'static':
        display_static()
    elif args.mode == 'single':
        display_random_singles()
    else:  # loop mode
        display_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting display")
