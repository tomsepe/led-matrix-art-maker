#include <Arduino.h>
#include <Wire.h>

/*
 * Dual I2C Bus Scanner
 * 
 * This scanner detects I2C devices on two separate I2C buses.
 * NOTE: This code requires hardware that supports multiple I2C buses!
 * 
 * Compatible Hardware:
 * - ESP32 boards (built-in dual I2C support)
 * - Raspberry Pi (with GPIO I2C configuration)
 * - Other MCUs with multiple I2C peripherals
 * 
 * Not Compatible:
 * - Arduino Uno, Nano, Metro Mini, or other basic Arduino boards
 *   with single I2C bus hardware
 * 
 * Default Pin Configurations (ESP32):
 * Bus 1 (Wire):  SDA = 21, SCL = 22
 * Bus 2 (Wire1): SDA = 19, SCL = 18
 */

// Function declarations
void I2C_ScannerWire();
void I2C_ScannerWire1();

void setup() {
  Serial.begin(115200);

  Wire.begin();        // Initialize primary I2C bus
  Wire1.begin(19, 18); // Initialize secondary I2C bus

  Serial.println("\nDual I2C Bus Scanner");
  Serial.println("-------------------");
  
  Serial.println("\n---------- Scanning Primary I2C Bus -------------");
  I2C_ScannerWire();

  Serial.println("\n---------- Scanning Secondary I2C Bus ------------");
  I2C_ScannerWire1();
}

void loop() { 
  delay(10); 
}

void I2C_ScannerWire() {
  byte error, address;
  int nDevices;

  Serial.println("Scanning...");

  nDevices = 0;
  for(address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.print(address, HEX);
      Serial.println("  !");

      nDevices++;
    }
    else if (error == 4) {
      Serial.print("Unknown error at address 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
    }    
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  }
  else {
    Serial.println("done\n");
  }
}

void I2C_ScannerWire1() {
  byte error, address;
  int nDevices;

  Serial.println("Scanning...");

  nDevices = 0;
  for(address = 1; address < 127; address++) {
    Wire1.beginTransmission(address);
    error = Wire1.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.print(address, HEX);
      Serial.println("  !");

      nDevices++;
    }
    else if (error == 4) {
      Serial.print("Unknown error at address 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
    }    
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  }
  else {
    Serial.println("done\n");
  }
} 