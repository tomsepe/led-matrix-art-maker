# CircuitPython Quickstart
## Follow this step-by-step to quickly get CircuitPython running on your board.
Download circuit python
https://circuitpython.org/board/adafruit_kb2040/

To enter the bootloader, hold down the BOOT/BOOTSEL button (highlighted in red above), and while continuing to hold it (don't let go!), press and release the reset button (highlighted in red or blue above). Continue to hold the BOOT/BOOTSEL button until the RPI-RP2 drive appears!

If the drive does not appear, release all the buttons, and then repeat the process above.

You can also start with your board unplugged from USB, press and hold the BOOTSEL button (highlighted in red above), continue to hold it while plugging it into USB, and wait for the drive to appear before releasing the button.

A lot of people end up using charge-only USB cables and it is very frustrating! Make sure you have a USB cable you know is good for data sync.

You will see a new disk drive appear called RPI-RP2.

Drag the adafruit_circuitpython_etc.uf2 file to RPI-RP2.

The RPI-RP2 drive will disappear and a new disk drive called CIRCUITPY will appear.

That's it, you're done!

## Safe Mode
You want to edit your code.py or modify the files on your CIRCUITPY drive, but find that you can't. Perhaps your board has gotten into a state where CIRCUITPY is read-only. You may have turned off the CIRCUITPY drive altogether. Whatever the reason, safe mode can help.

Safe mode in CircuitPython does not run any user code on startup, and disables auto-reload. This means a few things. First, safe mode bypasses any code in boot.py (where you can set CIRCUITPY read-only or turn it off completely). Second, it does not run the code in code.py. And finally, it does not automatically soft-reload when data is written to the CIRCUITPY drive.

Therefore, whatever you may have done to put your board in a non-interactive state, safe mode gives you the opportunity to correct it without losing all of the data on the CIRCUITPY drive.

### Entering Safe Mode
To enter safe mode when using CircuitPython, plug in your board or hit reset (highlighted in red above). Immediately after the board starts up or resets, it waits 1000ms. On some boards, the onboard status LED (highlighted in green above) will blink yellow during that time. If you press reset during that 1000ms, the board will start up in safe mode. It can be difficult to react to the yellow LED, so you may want to think of it simply as a slow double click of the reset button. (Remember, a fast double click of reset enters the bootloader.)

### In Safe Mode
If you successfully enter safe mode on CircuitPython, the LED will intermittently blink yellow three times.

If you connect to the serial console, you'll find the following message.

You can now edit the contents of the CIRCUITPY drive. Remember, your code will not run until you press the reset button, or unplug and plug in your board, to get out of safe mode.

## I2C Pin Configuration for LED Matrices

The KB2040 supports multiple I2C buses. Here are the recommended pin configurations for controlling LED matrices:

### First I2C Bus (Default)
```
SCL: board.SCL (Pin 3)
SDA: board.SDA (Pin 2)
```

### Second I2C Bus (Alternative)
```
SCL: board.A3 (Pin 26)
SDA: board.A2 (Pin 25)
```

### Connection Diagram

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

## Important Notes
1. Both I2C buses share the same power (3.3V) and ground
2. The KB2040 operates at 3.3V - ensure LED matrices are compatible
3. Set different I2C addresses for matrices on the same bus using A0, A1, A2 pins
4. Use a data-capable USB cable for programming and power
5. The board can be powered via USB or external 3.3V power supply

## I2C Address Configuration
For matrices on the same bus, set different addresses using the A0, A1, A2 pins:
- A0, A1, A2 all LOW (GND) = 0x70
- A0 HIGH (3.3V), A1, A2 LOW = 0x71
- A1 HIGH, A0, A2 LOW = 0x72
- A0, A1 HIGH, A2 LOW = 0x73
- A2 HIGH, A0, A1 LOW = 0x74
- A0, A2 HIGH, A1 LOW = 0x75
- A1, A2 HIGH, A0 LOW = 0x76
- A0, A1, A2 all HIGH = 0x77