# Adafruit KB2040 Setup Guide

## Table of Contents
1. [CircuitPython Installation](#circuitpython-installation)
2. [Using Mu Editor](#using-mu-editor)
3. [Safe Mode](#safe-mode)
4. [I2C Configuration](#i2c-configuration)
5. [Power Configuration](#power-configuration)

## CircuitPython Installation

1. Download CircuitPython for KB2040:
   https://circuitpython.org/board/adafruit_kb2040/

2. Enter Bootloader Mode:
   - Hold down the BOOT/BOOTSEL button
   - While holding BOOT/BOOTSEL, press and release the reset button
   - Continue holding BOOT/BOOTSEL until RPI-RP2 drive appears
   
   Alternative Method:
   - Start with board unplugged
   - Hold BOOT/BOOTSEL button
   - Plug in USB while holding button
   - Wait for RPI-RP2 drive to appear

3. Install CircuitPython:
   - Drag the downloaded .uf2 file to RPI-RP2 drive
   - Wait for CIRCUITPY drive to appear

> **Important**: Use a data-capable USB cable, not just a charging cable.

## Using Mu Editor

Mu Editor is the recommended development environment for CircuitPython.

### Installation
1. Download from https://codewith.mu/
2. Install following OS-specific instructions
3. Launch Mu Editor

### Setup
1. Connect KB2040 to computer
2. Click "Mode" button
3. Select "CircuitPython"
4. Click "Load" to view code.py

### Features
- **Serial Console**: View code output
- **Plotter**: Real-time data visualization
- **Files**: Manage CIRCUITPY drive
- **REPL**: Interactive Python console

### Tips
- Always save before running code
- Use serial console for debugging
- REPL is great for quick testing
- Code can be edited in safe mode

## Safe Mode

Safe mode bypasses user code and auto-reload, useful for fixing issues.

### Entering Safe Mode
1. Plug in board or press reset
2. Wait for yellow LED blink (1000ms)
3. Press reset during this window
   
> Think of it as a slow double-click of reset button.

### In Safe Mode
- LED blinks yellow three times
- Code.py doesn't run
- Files can be edited
- Press reset to exit

## I2C Configuration

The KB2040 supports multiple I2C buses for LED matrix control.

### Pin Configuration

#### First I2C Bus (Default)
```
SCL: board.SCL (Pin 3)
SDA: board.SDA (Pin 2)
```

#### Second I2C Bus (Alternative)
```
SCL: board.A3 (Pin 26)
SDA: board.A2 (Pin 25)
```

### Connection Diagrams

```
First LED Matrix Set (Default I2C Bus)
+------------------+     +------------------+
|     KB2040       |     |   LED Matrix     |
|                  |     |                  |
| Pin 3 (SCL) -----+-----+ SCL             |
| Pin 2 (SDA) -----+-----+ SDA             |
| 3.3V     --------+-----+ VCC             |
| GND      --------+-----+ GND             |
+------------------+     +------------------+

Second LED Matrix Set (Alternative I2C Bus)
+------------------+     +------------------+
|     KB2040       |     |   LED Matrix     |
|                  |     |                  |
| Pin 26 (A3) -----+-----+ SCL             |
| Pin 25 (A2) -----+-----+ SDA             |
| 3.3V     --------+-----+ VCC             |
| GND      --------+-----+ GND             |
+------------------+     +------------------+
```

### Important Notes
1. Both buses share 3.3V power and ground
2. KB2040 operates at 3.3V
3. Set different I2C addresses using A0, A1, A2 pins
4. Use data-capable USB cable
5. Can be powered via USB or external 3.3V

### I2C Address Configuration
| A2 | A1 | A0 | Address |
|----|----|----|---------|
| 0  | 0  | 0  | 0x70    |
| 0  | 0  | 1  | 0x71    |
| 0  | 1  | 0  | 0x72    |
| 0  | 1  | 1  | 0x73    |
| 1  | 0  | 0  | 0x74    |
| 1  | 0  | 1  | 0x75    |
| 1  | 1  | 0  | 0x76    |
| 1  | 1  | 1  | 0x77    |
```

## Power Configuration

### Board Power
- KB2040 operates at 3.3V
- Power via USB for programming and control
- GPIO pins are 3.3V logic level

### LED Matrix Power (5V)
LED matrices can be powered from a 5V source while keeping I2C signals at 3.3V:

```
+------------------+     +------------------+
|     KB2040       |     |   LED Matrix     |
|                  |     |                  |
| Pin 3 (SCL) -----+-----+ SCL             |
| Pin 2 (SDA) -----+-----+ SDA             |
| GND      --------+-----+ GND             |
|                  |     |                  |
|                  |     | VCC -----+       |
|                  |     |          |       |
|                  |     |          v       |
|                  |     |      5V Battery  |
+------------------+     +------------------+
```

### Important Notes
1. Keep I2C signals (SDA, SCL) at 3.3V
2. Connect GND between KB2040 and LED matrices
3. Power LED matrices from 5V battery
4. Do not connect 5V to any KB2040 pins
5. Use a common ground between all components

### Safety Considerations
- Always connect ground first
- Double-check voltage levels before connecting
- Use appropriate power supply for LED matrices
- Consider adding a fuse or current limiting resistor