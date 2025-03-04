# LED Matrix Art Maker

A tool for creating and displaying pixel art on LED matrix displays.

## Host Computer Setup (for bit-draw.py)

This is where you'll create your pixel art designs.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

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

# Install required packages
pip install pillow

# Install Adafruit libraries for LED matrix control
pip install adafruit-blinka
pip install adafruit-circuitpython-ht16k33
```

## Running the Programs

Make sure your virtual environment is activated on your Host computer before running any scripts:

```bash
# Create pixel art
python bit-draw.py
```

### On Raspberry Pi
```bash
# Display art on LED matrix
python led-matrix-show.py
```

Note: `led-matrix-show.py` requires physical LED matrix hardware connected to your Raspberry Pi.