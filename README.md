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

# Install Adafruit libraries for LED matrix control
pip install adafruit-blinka
pip install adafruit-circuitpython-ht16k33
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

### General Notes
- All matrices use maximum brightness (1.0) for optimal visibility
- I2C must be enabled on your Raspberry Pi
- Ensure proper power supply for the LED matrices
- Check I2C addresses match your hardware configuration