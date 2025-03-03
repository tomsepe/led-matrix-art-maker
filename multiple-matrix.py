#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

Adafruit_8x8matrix matrix = Adafruit_8x8matrix();
""" 
  matrix.begin(0x70);
  matrix.drawRect(0, 0, 8, 8, LED_ON); """

# With multiple matrices, we could declare each matrix object with a distinct name:
Adafruit_8x8matrix matrixOne   = Adafruit_8x8matrix();
Adafruit_8x8matrix matrixTwo   = Adafruit_8x8matrix();
Adafruit_8x8matrix matrixThree = Adafruit_8x8matrix();

""" But we’ll usually find it easier to declare an object array. 
There are three unique matrix addresses 
so we declare a three-element array: """

Adafruit_8x8matrix matrix[3] = {
  Adafruit_8x8matrix(),
  Adafruit_8x8matrix(),
  Adafruit_8x8matrix(),

};

for(uint8_t i=0; i<3; i++) {
    matrix[i] = Adafruit_8x8matrix();
    matrix[i].begin(0x70 + i);
}

""" 
To issue commands to a specific matrix, 
we follow the array name (“matrix”) with an index — 
the element number in the array (a four-element array
 has indices 0 through 2). The syntax and parameters 
 are otherwise the same as the single-matrix example.
 Here we issue different commands
 to each of three matrices in an array: 
 """
  matrix[0].drawPixel(0, 0, LED_ON);
  matrix[1].drawLine(0, 0, 7, 7, LED_ON);
  matrix[2].drawRect(0, 0, 8, 8, LED_ON);
 # matrix[3].fillRect(2, 2, 4, 4, LED_ON);