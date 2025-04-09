import board
import busio
import time

def print_pin_info():
    """Print information about all available pins"""
    print("\nAvailable pins on the board:")
    for pin_name in dir(board):
        if not pin_name.startswith('_') and not pin_name in ['ap_board', 'board_id', 'detector', 'pin', 'sys']:
            print(f"- {pin_name}")

def test_i2c_pins(scl_pin, sda_pin, description=""):
    try:
        print(f"\nTesting I2C with SCL={scl_pin}, SDA={sda_pin} {description}")
        i2c = busio.I2C(scl_pin, sda_pin)
        print("✅ Successfully initialized I2C!")
        i2c.deinit()
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False

print("=== I2C Pin Testing Script ===")
print("\n1. Listing all available pins:")
print_pin_info()

print("\n2. Testing known I2C pin combinations:")
# Test the default I2C pins first
test_i2c_pins(board.SCL, board.SDA, "(Default I2C pins)")

# Test other potential I2C pin combinations
pin_combinations = [
    (board.D1, board.D0, "GPIO 1, 0"),
    (board.D3, board.D2, "GPIO 3, 2"),
    (board.D10, board.D9, "GPIO 10, 9"),
    (board.D15, board.D14, "GPIO 15, 14"),
]

for scl, sda, desc in pin_combinations:
    test_i2c_pins(scl, sda, f"({desc})")
    time.sleep(1)  # Small delay between tests

print("\n3. Checking for I2C-related pins:")
i2c_related = [pin for pin in dir(board) if 'I2C' in pin or 'SCL' in pin or 'SDA' in pin]
print("I2C-related pins found:")
for pin in i2c_related:
    print(f"- {pin}")

print("\nNote: For a second I2C bus, you need to:")
print("1. Enable it in /boot/config.txt")
print("2. Use pins that support hardware I2C")
print("3. Ensure the pins aren't being used by other functions") 