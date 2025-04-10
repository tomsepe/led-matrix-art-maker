# LED Matrix Art Maker

A tool for creating and displaying 8x8 pixel art on LED matrix displays.

## Host Computer Setup (for bit-draw.py)

This is where you'll create your pixel art designs.

### MAC OS Instructions:
   First, find where you downloaded/extracted the LED Matrix Art Maker:
   - If you received it by email, check your Downloads folder
   - The folder should be named "led-matrix-draw.zip"
   - Double-click on the file to extract it
  
   - Open Terminal (Cmd + Space, type "terminal", press Enter)
   - Type "cd " (with a space after cd)
   - Drag and drop the "led-matrix-web" folder from Finder into Terminal
   - Press Enter
   - Now Terminal will open and you'll be working out of the proper directory
   - Now type:


```bash
python3 -m venv venv
```
This will create a virtual environment so we can install necessary library without affecting your computer's setup.

### Activate the virtual environment:
```bash
source venv/bin/activate
```
### Install required package
```bash
pip install pillow
```

## Creating Pixel Art

1. Run the pixel art creation tool:
```bash
python bit-draw.py
```
1. This will start the app and you can now draw your 8x8 pixel art designs
2. Save your designs - they will be stored in the `saved-drawings` directory
3. Send me the saved drawings and I'll convert them to work on the led matrix display

