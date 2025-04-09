import board
import busio
import time

def test_i2c_pins(scl_pin, sda_pin):
    try:
        print(f"\nTesting I2C with SCL={scl_pin}, SDA={sda_pin}")
        i2c = busio.I2C(scl_pin, sda_pin)
        print("Successfully initialized I2C!")
        i2c.deinit()
        return True
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False

# List of potential I2C pin combinations to test
pin_combinations = [
    (board.D1, board.D0),    # GPIO 1, 0
    (board.D3, board.D2),    # GPIO 3, 2
    (board.D10, board.D9),   # GPIO 10, 9
    (board.D45, board.D44),  # GPIO 45, 44
    (board.SCL, board.SDA),  # Default I2C pins
]

print("Testing I2C pin combinations...")
for scl, sda in pin_combinations:
    test_i2c_pins(scl, sda)
    time.sleep(1)  # Small delay between tests 