# Enable Multiple I2C Buses on Raspberry Pi

*Last updated: April 16, 2020*

This guide explains how to enable and configure multiple I2C buses on a Raspberry Pi 4 (2GB, rev 1.2) running the latest Raspbian Lite.

## Configuration Steps

### 1. Edit the Boot Configuration

Edit the boot config file:
```bash
sudo nano /boot/config.txt
```

Add or modify the following lines:
```bash
# Enable I2C interface
dtparam=i2c_arm=on

# Configure second I2C bus
dtoverlay=i2c-gpio,bus=2,i2c_gpio_sda=17,i2c_gpio_scl=27
```

Save the file by pressing:
- `Ctrl + X`
- `Y` to confirm
- `Enter` to save

### 2. Reboot the System

```bash
sudo reboot -h now
```

## Physical Connections

Connect your I2C devices as follows:

- **Bus 1 (Primary)**
  - SDA: GPIO 23
  - SCL: GPIO 24

- **Bus 2 (Secondary)**
  - SDA: GPIO 17
  - SCL: GPIO 27

## Testing the I2C Buses

To check devices on each bus:

For Bus 1:
```bash
i2cdetect -y 1
```

For Bus 2:
```bash
i2cdetect -y 2
```

These commands will show a grid of addresses where I2C devices are detected on each bus.