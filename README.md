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

## Raspberry Pi Setup (for led-matrix-show.py)

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
4. Save your designs - they will be stored in the `images` directory

## Converting Art to Patterns

After creating your pixel art, convert them to LED matrix patterns:
```bash
python convert-image-to-bytes.py
```
This will:
- Read all 8x8 PNG files from the `images` directory
- Convert them to LED matrix patterns
- Save them in `patterns/led_patterns.py`

## Displaying on LED Matrices

On your Raspberry Pi:
```bash
python led-matrix-show.py
```

The display will:
- Show random 8x8 patterns on each matrix
- Change patterns independently at random intervals (1-5 seconds)
- Continue until interrupted with Ctrl+C

## Hardware Setup

The script expects three 8x8 LED matrices connected via I2C with addresses:
- Left matrix: 0x70
- Middle matrix: 0x71
- Right matrix: 0x72

Display brightness is set to 50% by default and can be adjusted in the script.