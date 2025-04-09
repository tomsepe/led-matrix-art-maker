# LED Matrix Art Maker

A tool for creating and displaying 8x8 pixel art on LED matrix displays.

## Host Computer Setup (for bit-draw.py)

This is where you'll create your pixel art designs.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required package
pip install pillow
```

## Raspberry Pi Setup (for LED matrix display)

This is where you'll display your pixel art on the LED matrices.

```bash
# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install required libraries
pip install adafruit-blinka
pip install adafruit-circuitpython-ht16k33
pip install smbus2  # Required for multiple I2C bus support
```

## Creating Pixel Art

1. Activate your virtual environment on the host computer
2. Run the pixel art creation tool:
```bash
python bit-draw.py
```
3. Draw your 8x8 pixel art designs
4. Save your designs - they will be stored in the `saved-drawings` directory

## Converting Art to Patterns

After creating your pixel art, convert them to LED matrix patterns:
```bash
python convert-image-to-bytes.py
```
This will:
- Read all 8x8 PNG files from the `saved-drawings` directory
- Convert them to LED matrix patterns
- Save them in `patterns/led_patterns.py`

## Displaying on LED Matrices

The project includes several display scripts for different configurations:

### Single Matrix Display
```bash
python led-1xmatrix-show.py
```
- Displays patterns on a single 8x8 LED matrix
- Changes patterns every 1-5 seconds
- Runs until interrupted with Ctrl+C

### Three Matrix Display
```bash
python led-1x3matrix-show.py
```
- Displays patterns on three 8x8 LED matrices
- Each matrix changes patterns independently
- Changes patterns every 1-5 seconds
- Runs until interrupted with Ctrl+C

### Six Matrix Display (Dual I2C Bus)
```bash
python led-2x3matrix-show.py
```
- Displays patterns on six 8x8 LED matrices using two I2C buses
- Each matrix changes patterns independently
- Changes patterns every 1-5 seconds
- Runs until interrupted with Ctrl+C
- Requires additional I2C bus configuration (see Hardware Setup)

### Fast Display (Experimental)
```bash
python fast.py
```
- Optimized version for faster pattern updates
- Uses more efficient pixel setting methods
- Suitable for both single and multiple matrix setups

## Hardware Setup

### Single Matrix Setup
- Connect one 8x8 LED matrix via I2C
- Default address: 0x70

### Three Matrix Setup
Connect three 8x8 LED matrices via I2C with addresses:
- Left matrix: 0x70
- Middle matrix: 0x71
- Right matrix: 0x72

### Six Matrix Setup (Dual I2C Bus)
This setup requires two separate I2C buses:

1. Enable the second I2C bus by adding to `/boot/config.txt`:
```bash
# Enable I2C interface
dtparam=i2c_arm=on

# Configure second I2C bus
dtoverlay=i2c-gpio,bus=2,i2c_gpio_sda=17,i2c_gpio_scl=27
```

2. Connect the matrices:
- First set (Bus 1):
  - Left matrix: 0x70
  - Middle matrix: 0x71
  - Right matrix: 0x72
- Second set (Bus 2):
  - Left matrix: 0x70
  - Middle matrix: 0x71
  - Right matrix: 0x72

3. Reboot the Raspberry Pi after making changes to `/boot/config.txt`

### General Notes
- All matrices use maximum brightness (1.0) for optimal visibility
- I2C must be enabled on your Raspberry Pi
- Ensure proper power supply for the LED matrices
- Check I2C addresses match your hardware configuration
- For multiple I2C bus setups, verify connections with `i2cdetect -y 1` and `i2cdetect -y 2`