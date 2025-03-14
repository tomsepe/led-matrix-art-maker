import board
from adafruit_ht16k33.matrix import Matrix8x8
import time
import random
from patterns.led_patterns import PATTERNS

"""
Example pattern format in patterns/led_patterns.py:

PATTERNS = {
    'pixel_art_20240220_123456': bytes([
        # 8x8 matrix pattern (1 = LED on, 0 = LED off)
        0b11000011,  # Row 0: ■■○○○○■■
        0b11000011,  # Row 1: ■■○○○○■■
        0b00111100,  # Row 2: ○○■■■■○○
        0b00111100,  # Row 3: ○○■■■■○○
        0b00111100,  # Row 4: ○○■■■■○○
        0b00111100,  # Row 5: ○○■■■■○○
        0b11000011,  # Row 6: ■■○○○○■■
        0b11000011,  # Row 7: ■■○○○○■■
    ]),
    # ... more patterns ...
}
"""

# Initialize I2C and matrix
i2c = board.I2C()
matrix = Matrix8x8(i2c, address=0x70)  # Default address is 0x70

# Set brightness (0.0 to 1.0)
matrix.brightness = 0.5
matrix.blink_rate = 0

def display_pattern(pattern_data):
    """Display an 8x8 pattern on the matrix"""
    try:
        # Set all pixels
        for row, byte_val in enumerate(pattern_data):
            for col in range(8):
                matrix[col, row] = (byte_val >> (7 - col)) & 1
        matrix.show()
        return True
    except Exception as e:
        print(f"Error displaying pattern: {e}")
        return False

def main():
    print("Starting 8x8 LED Matrix Display...")
    print("Press Ctrl+C to exit")
    
    # Get list of patterns
    pattern_names = sorted(PATTERNS.keys())
    if not pattern_names:
        print("No patterns available in patterns/led_patterns.py")
        return
        
    # Display random patterns
    while True:
        try:
            # Choose random pattern
            pattern_name = random.choice(pattern_names)
            pattern_data = PATTERNS[pattern_name]
            
            # Display pattern
            if display_pattern(pattern_data):
                print(f"Displaying: {pattern_name}")
            
            # Wait random time (1-5 seconds)
            time.sleep(random.randint(1, 5))
            
        except KeyboardInterrupt:
            print("\nExiting display")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
